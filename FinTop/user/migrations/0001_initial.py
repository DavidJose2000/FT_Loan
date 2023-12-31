# Generated by Django 3.2.4 on 2021-09-20 11:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=20)),
                ('number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Please enter valid phone number. Correct format is 04XXXXXXXX', regex='^\\+?1?\\d{9,15}$')])),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=2500)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Inbox',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_status', models.CharField(blank=True, max_length=15, null=True)),
                ('loan_wname', models.CharField(blank=True, max_length=15, null=True)),
                ('loan_wphone', models.CharField(blank=True, max_length=20, null=True)),
                ('loan_wemail', models.CharField(blank=True, max_length=40, null=True)),
                ('loan_type', models.CharField(choices=[('Buy a Home', 'Buy a Home'), ('Refinance', 'Refinance')], max_length=15)),
                ('vehicle', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25)),
                ('vehicle_worth', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('vehicle_money', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('carloan_pay', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25, null=True)),
                ('accounts', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('superannuation', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('additional_asset', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25)),
                ('home_content', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('credit_card', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25)),
                ('credit_limit', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('liability_loan', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=25)),
                ('loans', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('employment_type', models.CharField(choices=[('Employee', 'Employee'), ('Self-employed', 'Self-employed'), ('Not working', 'Not working')], max_length=50)),
                ('annual_salary', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('monthly_expense', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bizpartner', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'BizPartner',
            },
        ),
        migrations.CreateModel(
            name='Underprocess_loans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=15, null=True)),
                ('commissions', models.CharField(max_length=20)),
                ('commission_status', models.CharField(max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('referred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bizpartner Commissions',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UnitNumber', models.CharField(max_length=50)),
                ('HouseNumber', models.CharField(max_length=50)),
                ('StreetName', models.CharField(max_length=50)),
                ('SuburbName', models.CharField(max_length=50)),
                ('PinCode', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('State', models.CharField(max_length=50)),
                ('Country', models.CharField(max_length=50)),
                ('LastSoldPrice', models.IntegerField()),
                ('LastSoldDate', models.DateTimeField()),
                ('ExpectedPrice', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phnumber', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter valid phone number. Correct format is 04XXXXXXXX', regex='^\\+?1?\\d{9,15}$')])),
                ('email_confirmed', models.BooleanField(default=False)),
                ('is_bizpartner', models.BooleanField(default=False)),
                ('is_agent', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile Verification',
            },
        ),
        migrations.CreateModel(
            name='Incoming_loans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Completed_Loans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('signature', models.CharField(max_length=50)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='BizpartnerAgreement/')),
                ('status', models.CharField(max_length=50, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bizpartner Data',
            },
        ),
        migrations.CreateModel(
            name='BankInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankname', models.CharField(max_length=50)),
                ('acname', models.CharField(max_length=50)),
                ('acno', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('bankisc', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[0-9]*$', message='Only numbers are allowed.')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agent_Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Additional_liabilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(blank=True, choices=[('tax debt', 'tax debt'), ('other lines of credit', 'other lines of credit')], max_length=35, null=True)),
                ('owned', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.loan')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Additional_assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(choices=[('Term Deposit', 'Term Deposit'), ('Shares', 'Shares'), ('Managed Funds', 'Managed Funds'), ('Gifts', 'Gifts')], max_length=35)),
                ('description', models.CharField(blank=True, max_length=25, null=True)),
                ('total_value', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.loan')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Additional_assets',
                'verbose_name_plural': 'Additional_assets',
            },
        ),
    ]
