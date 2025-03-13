from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('naturapeute', '0030_alter_therapist_invoice_data'),
    ]
    operations = [
        migrations.AddField(
            model_name='therapist',
            name='calendly_url',
            field=models.URLField(blank=True, help_text='URL Calendly du thérapeute', max_length=255, null=True),
        ),
    ]