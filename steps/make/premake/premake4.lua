solution("PROJECT_NAME")
    configurations {"Debug", "Release"}

    targetdir("bin")

    configuration "debug"
        defines { "DEBUG" }
        flags { "Symbols" }
    configuration "release"
        defines { "NDEBUG" }
        flags { "OptimizeSpeed" }

    project("PROJECT_NAME")
        --uuid("")
        kind("WindowedApp")
        language("C++")
        links {
        }
        files {
            "src/**.h",
            "src/**.cpp"
        }
        excludes {
        }
        includedirs {
            "vendor/include/",
            "/usr/local/include/",
        }
        libdirs {
            "/usr/local/lib/",
            "/usr/local/lib64/",
        }
        
        buildoptions {
        }
        linkoptions {
        }
        configuration {"debug"}
            links {}
        configuration {}

        configuration { "gmake" }
            buildoptions { "-std=c++11" }
            --buildoptions { "-std=c++11",  "-pedantic", "-Wall", "-Wextra" }
            configuration { "macosx" }
                buildoptions { "-U__STRICT_ANSI__", "-stdlib=libc++" }
                linkoptions { "-stdlib=libc++" }
        configuration {}


