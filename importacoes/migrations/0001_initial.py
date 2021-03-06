# Generated by Django 3.2.5 on 2022-04-11 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Importacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_importacao', models.DateTimeField(verbose_name='Data e hora da importação')),
                ('data_transacao', models.DateField(verbose_name='Data da transação')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
            },
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco_origem', models.CharField(max_length=100, verbose_name='Banco de origem')),
                ('agencia_origem', models.CharField(max_length=6, verbose_name='Agência de origem')),
                ('conta_origem', models.CharField(max_length=10, verbose_name='Conta de origem')),
                ('banco_destino', models.CharField(max_length=100, verbose_name='Banco de destino')),
                ('agencia_destino', models.CharField(max_length=6, verbose_name='Agência de destino')),
                ('conta_destino', models.CharField(max_length=10, verbose_name='Conta de destino')),
                ('valor_transacao', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor da transação')),
                ('data_hora_transação', models.DateTimeField(verbose_name='Data e hora da transação')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
            },
        ),
    ]
