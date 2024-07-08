pip install huggingface_hub
cd /data/workspace
git clone https://github.com/NVIDIA/megatron-lm.git
# Change Hugging Face cache directory
export HF_HOME=/data/huggingface
echo "export HF_HOME=/data/huggingface" >> ~/.bashrc


pip install nltk numpy parameterized pybind11 regex six tensorboard transformers 'black==21.4b0' 'isort>=5.5.4'

#prepare the training of gpt-2

mkdir -p Models/gpt-2/data
cd Models/gpt-2/data

wget https://huggingface.co/bigscience/misc-test-data/resolve/main/stas/oscar-1GB.jsonl.xz
wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-vocab.json
wget https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-merges.txt

xz -d oscar-1GB.jsonl.xz
cd ..

python ../../megatron-lm/tools/preprocess_data.py \
  --input ./data/oscar-1GB.jsonl \
  --output-prefix meg-gpt2 \
  --vocab-file ./data/gpt2-vocab.json \
  --tokenizer-type GPT2BPETokenizer \
  --merge-file ./data/gpt2-merges.txt \
  --append-eod \
  --workers 8
mv meg-gpt2* ./data

apt update
apt install net-tools
netstat -anop | grep tcp
