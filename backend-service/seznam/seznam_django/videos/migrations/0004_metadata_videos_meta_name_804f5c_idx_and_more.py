# Generated by Django 4.1.7 on 2023-03-12 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_drm_feature_metadata_delete_video'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='metadata',
            index=models.Index(fields=['name'], name='videos_meta_name_804f5c_idx'),
        ),
        migrations.AddIndex(
            model_name='metadata',
            index=models.Index(fields=['short_name'], name='videos_meta_short_n_fecbe1_idx'),
        ),
        migrations.AddIndex(
            model_name='metadata',
            index=models.Index(fields=['complete_json'], name='videos_meta_complet_5a7c34_idx'),
        ),
    ]
