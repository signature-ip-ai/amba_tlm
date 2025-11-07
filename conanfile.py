#!/bin/env python3

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout

class ambatlm(ConanFile):
    name = "ambatlm"
    version = "20230601"
    systemc_version = "3.0.1"
    cmake_version = "3.31.6"

    license = "The Clear BSD License"
    author = "Arm Limited (or its affiliates)"
    url = "http://gitlab.marqueesemi.com:8081/sw-tools/amba-tlm"
    description = "The Arm AMBA Transaction-Level Modeling (TLM) library allows you to model and simulate approximately-timed (AT) and cycle-accurate (CA) AXI4 and ACE ports"
    topics = ("AMBA ARM", "TLM", "AXI4", "SystemC")

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }

    default_options = {
        "shared": False,
        "fPIC": True,

        f"systemc/{systemc_version}:fPIC": True,
        f"systemc/{systemc_version}:shared": False,
        f"systemc/{systemc_version}:enable_pthreads": False,
        f"systemc/{systemc_version}:enable_assertions": True,
        f"systemc/{systemc_version}:disable_virtual_bind": True,
        f"systemc/{systemc_version}:disable_async_updates": False,
        f"systemc/{systemc_version}:disable_copyright_msg": True,
        f"systemc/{systemc_version}:enable_phase_callbacks": True,
        f"systemc/{systemc_version}:enable_phase_callbacks_tracing": False,
        f"systemc/{systemc_version}:enable_immediate_self_notifications": False,
    }

    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "include/*",
        "doc/*",
        "test_package/*",
        "conafile.py",
        "README.md")


    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC


    def layout(self):
        cmake_layout(self)


    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.user_presets_path = False
        tc.generate()


    def requirements(self):
        self.requires(f"systemc/{self.systemc_version}")


    def build_requirements(self):
        self.tool_requires(f"cmake/{self.cmake_version}") #pylint: disable=not-callable


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()


    def package(self):
        cmake = CMake(self)
        cmake.install()


    def package_info(self):
        self.cpp_info.components["armtlmaxi4"].libs = ["armtlmaxi4"]
        self.cpp_info.components["armtlmchi"].libs = ["armtlmchi"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
