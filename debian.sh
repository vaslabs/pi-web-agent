cp .goreleaser.yml target/
cd target
unzip piwebagent2.zip
mv .goreleaser.yml piwebagent2/
cp -r ../scripts piwebagent2/
cd piwebagent2

goreleaser --snapshot --skip-publish

cd ../..