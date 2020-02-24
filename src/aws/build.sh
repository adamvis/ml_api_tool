# Parse arguments
while getopts m:b:n: option
do
case "${option}"
in
m) MODEL_DIR=${OPTARG};;
b) BUILD_DIR=${OPTARG};;
n) MODEL_NAME=${OPTARG};;
esac
done

# Build base directory
printf "Downloading Base Directory.."
svn export --force https://github.com/awslabs/amazon-sagemaker-examples/trunk/advanced_functionality/scikit_bring_your_own/container $BUILD_DIR > logs.txt
echo "done"

printf "Copying your model inside it.."
# Rename and fill model directory
mv $BUILD_DIR/decision_trees $BUILD_DIR/model > logs.txt
cp -r $MODEL_DIR $BUILD_DIR/model/src > logs.txt
touch $BUILD_DIR/model/__init__.py
rm logs.txt

# [REPL] - buil_and_push.sh
sed -i '' -e "s/decision_trees/model/g" $BUILD_DIR/build_and_push.sh
sed -i '' -e "s/us-west-2/us-east-1/g" $BUILD_DIR/build_and_push.sh

# [REPL] - Dockerfile
sed -i '' -e "s/ubuntu:16.04/python:3.6/g" $BUILD_DIR/Dockerfile
sed -i '' -e "s/Amazon AI <sage-learner@amazon.com>/Adam Viscusi <adam.viscusi@blackstraw.ai>/g" $BUILD_DIR/Dockerfile

awk '/ENV PATH="\/opt\/program:\${PATH}"/ { print; print "RUN mkdir -p \/opt\/ml\/output"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

awk '/RUN mkdir -p \/opt\/ml\/output/ { print; print "RUN mkdir -p \/opt\/ml\/input"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

awk '/# image, which reduces start up time./ { print; print "CMD [ \"\/bin\/bash\", \"source activate base\" ]"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

sed -i '' -e "s/decision_trees/model/g" $BUILD_DIR/Dockerfile

## [ADD-UNDER] COPy model opt/program
awk '/COPY model \/opt\/program/ { print; print "RUN chmod +x \/opt\/program\/train \/opt\/program\/serve"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

awk '/COPY model \/opt\/program/ { print; print "RUN pip3 install -r opt\/program\/src\/requirements.txt"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

awk '/COPY model \/opt\/program/ { print; print "RUN pip3 install flask gevent gunicorn imbalanced-learn==0.4.3 dill==0.2.9 boto3 psycopg2-binary joblib==0.13.2"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

awk '/COPY model \/opt\/program/ { print; print "RUN pip3 install --upgrade pip"; next }1' $BUILD_DIR/Dockerfile > $BUILD_DIR/Dockerfile.tmp
mv $BUILD_DIR/Dockerfile.tmp $BUILD_DIR/Dockerfile

sed -i '' -e '23,26d' $BUILD_DIR/Dockerfile
sed -i '' -e '12d' $BUILD_DIR/Dockerfile

# [REPL] - model/train
sed -i '' -e "s/from sklearn import tree/from src import Model/g" $BUILD_DIR/model/train
sed -i '' -e "s/input\/config\/hyperparameters.json/..\/program\/src\/hyperparameters.json/g" $BUILD_DIR/model/train
sed -i '' -e "s/tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)/Model(**trainingParams)/g" $BUILD_DIR/model/train
sed -i '' -e "s/train_X, train_y/train_data/g" $BUILD_DIR/model/train
sed -i '' -e "s/decision-tree-model.pkl/${MODEL_NAME}_model.pkl/g" $BUILD_DIR/model/train
sed -i '' -e '51,60d' $BUILD_DIR/model/train

# [REPL] - model/predictor.py
sed -i '' -e "s/decision-tree-model.pkl/${MODEL_NAME}_model.pkl/g" $BUILD_DIR/model/predictor.py

echo "done"

printf "Setting up testing environment.."
rm $BUILD_DIR/local_test/test_dir/model/decision-tree-model.pkl
rm $BUILD_DIR/local_test/test_dir/input/config/hyperparameters.json 
rm $BUILD_DIR/local_test/test_dir/input/data/training/iris.csv
cp ${MODEL_DIR}/hyperparameters.json $BUILD_DIR/local_test/test_dir/input/config/
cp ${MODEL_DIR}/test_data.csv $BUILD_DIR/local_test/test_dir/input/data/training/
echo "done"
