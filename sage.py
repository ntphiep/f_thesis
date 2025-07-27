import sagemaker
from sagemaker.huggingface import HuggingFace

role = "arn:aws:iam::014498663963:role/service-role/AmazonSageMaker-ExecutionRole-20250504T220510"

huggingface_estimator = HuggingFace(
    entry_point='train.py',
    source_dir='code',
    instance_type='ml.g5.xlarge',
    instance_count=1,
    role=role,
    transformers_version='4.49.0',
    pytorch_version='2.5.1',
    py_version='py311',
    hyperparameters={
        'model_name': 'VietAI/vit5-base',
        'dataset_name': 'ntphiep/vit5-tst-data-casual',  # HuggingFace dataset
        'epochs': 2,
        'per_device_train_batch_size': 8
    },
    base_job_name='vit5-finetune',
    disable_profiler=True,
    max_run=3600*3,
    output_path='s3://hiep-delta-bk/models/'
)

huggingface_estimator.fit()