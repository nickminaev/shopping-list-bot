#!/bin/bash

# Reference: https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-docker-image

src_path="../lambdas/src/$1"
if [[ ! -d $src_path ]]; then
    echo "Directory at path $src_path does not exist. Use one of the existing lambda names:"
    pushd ../lambdas/src > /dev/null
    ls -dl * | awk '{print $9}'
    popd > /dev/null
    exit 1
fi
echo "Switching to $src_path"
pushd $src_path >> /dev/null
echo "Exporing the UV dependencies into the requirements.txt file"
uv export --frozen --no-emit-workspace --no-emit-project --no-dev --no-editable --no-hashes -o requirements.txt
mkdir lambda_package
echo "Installing the dependencies into the local lambda_package directory"
uv pip install -r requirements.txt --target lambda_package
echo "Done installing the dependencies into the lambda_package directory. Copying the source code into it"
cp *.py lambda_package/
package_size=$(du -sh lambda_package | awk '{print $1}' | grep -Eo [0-9]*)
size_units=$(du -sh lambda_package | awk '{print $1}' | grep -Eo [A-Za-z]+)
case $size_units in 
    K)
        echo "The package size is below 250MB, which satisfies the AWS requirements."
        ;;
    M)
        if [[ $package_size -ge 250 ]]; then
        echo "Lambda package cannot exceed 250MB in the unzipped state. Aborting the build. Upload the file into an S3 bucket instead and refer in the Lambda config."
        exit 1
        fi
        echo "The package size is below 250MB, which satisfies the AWS requirements."
        ;;
    *)
        echo "Lambda package cannot exceed 250MB in the unzipped state. Aborting the build. Upload the file into an S3 bucket instead and refer in the Lambda config."
        exit 1
        ;;
esac
zip -r lambda_package.zip lambda_package >> /dev/null
chmod 644 lambda_package.zip
# aws lambda update-function-code --function-name $1 \
# --zip-file fileb://lambda_package.zip


