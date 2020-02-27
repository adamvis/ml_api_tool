# Parse arguments
while getopts b:n: option
do
case "${option}"
in
b) BUILD_DIR=${OPTARG};;
n) MODEL_NAME=${OPTARG};;
t) TAG=${OPTARG};;
esac
done


sh ${BUILD_DIR}/build_and_push.sh "${MODEL_NAME}-estimator" ${TAG}



