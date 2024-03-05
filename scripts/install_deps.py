import os
import argparse
import sys

def install_packages():
    commands = [
        "apt-get update",
        "apt-get install -y build-essential cmake git wget unzip g++ python3 libgtest-dev libyaml-cpp-dev libsuitesparse-dev libboost-all-dev ninja-build"
    ]
    for command in commands:
        if os.system(command) != 0:
            print("Error executing command: " + command)
            sys.exit(1)

def chdir(path):
    try:
        os.chdir(path)
    except Exception as e:
        print("Error changing directory to {}: {}".format(path, e))
        sys.exit(1)

def command(command):
    if os.system(command) != 0:
        print("Error executing command: " + command)
        sys.exit(1)

def mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

def install_eigen(thirdparty_dir):
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)
    
    command("git clone https://gitlab.com/libeigen/eigen.git")
    chdir("eigen")
    command("git checkout 3.2.9")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja ..")
    command("ninja")
    command("ninja install")


def install_opencv(thirdparty_dir):
    print("\nINSTALLING OPENCV....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    # Dependencies [GUI]
    command("apt-get install -y libgtkglext1-dev libvtk6-dev")
    # Dependencies [Media I/O]
    command("apt-get install -y zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libjasper-dev libopenexr-dev libgdal-dev")
    # Dependencies [Video I/O]
    command("apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev")
    # Dependencies [Parallelism and Linear Algebra]
    command("apt-get install -y libtbb-dev libeigen3-dev")
    # Dependencies [Python]
    command("apt-get install -y python-dev python-tk python-numpy python3-tk python3-numpy")
    # OpenCV contrib 3.2.0
    command("git clone https://github.com/opencv/opencv_contrib.git")
    chdir("opencv_contrib")
    command("git checkout 3.2.0")
    chdir("..")    
    # OpenCV 3.2.0
    command("git clone https://github.com/opencv/opencv.git")
    chdir("opencv")
    command("git checkout 3.2.0")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -DWITH_CUDA=OFF -DBUILD_EXAMPLES=OFF .. && ninja")
    command("ninja install")

def install_g2o(thirdparty_dir):
    print("\nINSTALLING G2O....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("git clone https://github.com/RainerKuemmerle/g2o.git")
    chdir("g2o")
    command("git checkout 4b9c2f5b68d14ad479457b18c5a2a0bce1541a90")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")
    

def install_dlib(thirdparty_dir):
    print("\nINSTALLING DLIB....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("git clone https://github.com/dorian3d/DLib.git")
    chdir("DLib")
    command("git checkout 70089a38056e8aebd5a2ebacbcb67d3751433f32")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")
    

def install_dbow2(thirdparty_dir):
    print("\nINSTALLING DBOW2....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("git clone https://github.com/dorian3d/DBoW2.git")
    chdir("DBoW2")
    command("git checkout 82401cad2cfe7aa28ee6f6afb01ce3ffa0f59b44")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")


def install_dloop_detector(thirdparty_dir):
    print("\nINSTALLING DLOOP DETECTOR....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("git clone https://github.com/dorian3d/DLoopDetector.git")
    chdir("DLoopDetector")
    command("git checkout 8e62f8ae84d583d9ab67796f779272b0850571ce")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")


def install_opengv(thirdparty_dir):
    print("\nINSTALLING OPENGV....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("git clone https://github.com/laurentkneip/opengv.git")
    chdir("opengv")
    command("git checkout 2e2d21917fd2fb75f2134e6d5be7a2536cbc7eb1")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")
    

def install_gtest(thirdparty_dir):
    print("\nINSTALLING GTEST....\n")
    mkdir(thirdparty_dir)
    chdir(thirdparty_dir)

    command("apt-get install libgtest-dev")
    chdir("/usr/src/gtest")
    command("cmake -GNinja -DBUILD_SHARED_LIBS=ON")
    command("ninja")
    command("cp *.so /usr/lib/")
    '''
    command("git clone https://github.com/google/googletest.git")
    chdir("googletest")
    command("git checkout release-1.8.1")
    mkdir("build")
    chdir("build")
    command("cmake -GNinja .. && ninja")
    command("ninja install")
    '''
    

def main():
    parser = argparse.ArgumentParser(description="Install thirdparty libraries into source_directory/thirdparty")
    parser.add_argument("source_dir", help="Path to the source directory")
    args = parser.parse_args()
    thirdparty_dir = os.path.join(os.path.abspath(args.source_dir), 'thirdparty')

    try:
        install_packages()
        install_eigen(thirdparty_dir)
        install_opencv(thirdparty_dir)
        install_g2o(thirdparty_dir)
        install_dlib(thirdparty_dir)
        install_dbow2(thirdparty_dir)
        install_dloop_detector(thirdparty_dir)
        install_opengv(thirdparty_dir)
        install_gtest(thirdparty_dir)
    except Exception as e:
        print("An error occurred: {}".format(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()