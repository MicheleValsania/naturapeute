from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('naturapeute', '0028_alter_therapist_languages'),
    ]
    operations = [
        migrations.AddField(
            model_name='therapist',
            name='calendly_url',
            field=models.URLField(blank=True, help_text='URL Calendly du thérapeute', max_length=255, null=True),
        ),
    ]