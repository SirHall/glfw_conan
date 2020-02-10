from conans import ConanFile, CMake, tools


class GLFWConan(ConanFile):
    name = "glfw"
    version = "0.0.1"
    license = "GPL3"
    author = ""
    url = "https://www.glfw.org/"
    requires = []
    description = "A multi-platform library for OpenGL, OpenGL ES, Vulkan, window and input"
    topics = ("graphics", "glfw", "opengl")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "include/**"

    def source(self):
        git = tools.Git(folder="glfw")
        print("Cloning https://github.com/glfw/glfw.git")
        git.clone("https://github.com/glfw/glfw.git", branch="master", shallow=True)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("glfw/CMakeLists.txt", "project(GLFW VERSION 3.4.0 LANGUAGES C)",
                              '''project(GLFW VERSION 3.4.0 LANGUAGES C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="glfw")
        print("Building glfw")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/",
                  src="glfw/include/", keep_path=True)
        self.copy("*.hpp", dst="include/",
                  src="glfw/include/", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["glfw3"]
