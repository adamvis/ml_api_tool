# Parse arguments
while getopts m:b:n: option
do
case "${option}"
in

n) MODEL_NAME=${OPTARG};;
i) TRAINING_IMAGE=${OPTARG};;
t) TRAINING_CONFIG_FILE=${OPTARG};;
esac
done

source $TRAINING_CONFIG_FILE

aws sagemaker create-training-job \
    --training-job-name "training_[${MODEL_NAME}]_${date +%d}_${date +%b}_${date +%H}_${date +%M}"\
    --algorithm-specification \
        TrainingImage=${TRAINING_IMAGE},TrainingInputMode=File \
    --role-arn <Role ARN> \
    --input-data-config \
        '{"ChannelName":"training", 
          "DataSource":{"S3DataSource":{"S3DataType":"S3Prefix", 
                                        "S3Uri":${TRAINING_DATA_PATH},
                                        "S3DataDistributionType":"FullyReplicated"
                                        } 
                        } 
          }' \
    --output-data-config \
        S3OutputPath=${OUTPUT_PATH} \
    --resource-config \
        InstanceType=ml.m4.xlarge,InstanceCount=1,VolumeSizeInGB=1 \
    --stopping-condition \
        MaxRuntimeInSeconds=86400 \
    --hyper-parameters \
        max_leaf_nodes=5 