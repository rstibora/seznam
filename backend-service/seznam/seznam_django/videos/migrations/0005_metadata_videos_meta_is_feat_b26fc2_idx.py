# Generated by Django 4.1.7 on 2023-03-12 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_metadata_videos_meta_name_804f5c_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='metadata',
            index=models.Index(fields=['is_featured'], name='videos_meta_is_feat_b26fc2_idx'),
        ),
    ]
