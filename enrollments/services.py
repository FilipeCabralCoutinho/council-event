import pandas as pd
from .models import Inscricoes, Pagamento, Parcela
import io
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .messages import text_fallback_new, start_text_new, text_fallback_payment_confirmation, start_text_payment_confirmation
from threading import Thread
from .logging import logger


class Services:
    @staticmethod
    def export_to_excel(self):
        logger.info("export_to_excel method initialized!")

        enrollments = Inscricoes.objects.order_by("id")

        data = []

        for i in enrollments:
            data.append(
                {
                    "ID": i.id,
                    "Nome": i.nome,
                    "CPF": i.cpf,
                    "Email": i.email,
                    "Celular": i.whatsapp,
                    "Distrito": i.distrito.nome,
                    "Igreja": i.igreja.nome,
                    "Função": i.funcao,
                    "Status Pagamento": i.status_pagamento,
                    "Apto Concílio?": i.apto_concilio,
                    "Possui Comorbidade?": i.possui_comorbidade,
                    "Qual Comorbidade?": i.qual_comorbidade,
                    "Vai Dormir no Efraim?": i.pernoite,
                    "Data/Hora Criação": i.created_at.strftime('%d/%m/%Y %H:%M'),
                    "Data/Hora Atualização": i.updated_at.strftime('%d/%m/%Y %H:%M'),
                    "Consentimento Dados": i.consent_given,
                    "IP_USER": i.ip_address
                }
            )

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Inscritos')

        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="inscricoes_concilio.xlsx"'

        logger.info("Excel obtained with success!")

        return response
    
    def _send_email(self, enrollment_id, email_type='new_enrollment'):
        try:
            enrollment = Inscricoes.objects.get(id=enrollment_id)
            now = timezone.localtime(timezone.now())

            logger.info(f"Sending {email_type} email for enrollment id {enrollment.id}. Hour: {now}")

            # Configurações por tipo de email
            email_config = {
                'new_enrollment': {
                    'subject': "Confirmação de inscrição – IX Concílio da 6ª Região",
                    'text_fallback': text_fallback_new(enrollment),
                    'text_title': "Recebemos sua inscrição 🙌",
                    'text_head': "Confirmação de inscrição ✅",
                    'start_text': start_text_new(),
                    'template': 'emails/enrollment_email.html',
                    'PIX_KEY': settings.PIX_KEY
                },
                'payment_confirmation': {
                    'subject': "Pagamento confirmado – IX Concílio da 6ª Região",
                    'text_fallback': text_fallback_payment_confirmation(enrollment),
                    'text_title': "Pagamento confirmado! ✅",
                    'text_head': "Confirmação de Pagamento",
                    'start_text': start_text_payment_confirmation(),
                    'template': 'emails/payment_confirmation_email.html'
                }
            }

            config = email_config.get(email_type, email_config['new_enrollment'])

            html_content = render_to_string(config['template'], {
                'enrollment': enrollment,
                "text_head": config['text_head'],
                "text_title": config['text_title'],
                "start_text": config['start_text'],
                "PIX_KEY": config.get('PIX_KEY'),
            })

            email = EmailMultiAlternatives(
                config['subject'],
                config['text_fallback'],
                f"IX Concílio da 6ª Região <{settings.EMAIL_HOST_USER}>",
                [enrollment.email]
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            logger.info(f"Email ({email_type}) sent for enrollment id: {enrollment.id}")

            enrollment.last_email = now
            enrollment.save()
        except Exception as e:
            logger.error(f"Error sending {email_type} email for enrollment id {enrollment_id}: {str(e)}", exc_info=True)

    def send_email(self, enrollment, email_type='new_enrollment'):
        logger.info(f"send_email initialized for id: {enrollment.id}, type: {email_type}")

        try:
            Thread(
                target=self._send_email, args=(enrollment.id, email_type)
            ).start()

            logger.info(f"Thread created with success for id: {enrollment.id}, type: {email_type}")

        except Exception as e:
            logger.error(f"Error when trying create Thread for id: {enrollment.id}, type: {email_type}")
            raise e
    
    def payment(self, instance_id):
        logger.info(f"Initialized paymento method for id: {instance_id}")
        instance = Inscricoes.objects.get(id=instance_id)

        if instance.pernoite == "SIM":
            valor_total = 720
        else:
            valor_total = 630

        qtd = instance.quantidade_parcelas
        valor_parcela = valor_total / qtd

        pagamento = Pagamento.objects.create(
            inscricao=instance,
            valor_total=valor_total
        )

        for i in range(1, qtd + 1):
            Parcela.objects.create(
                pagamento=pagamento,
                numero=i,
                valor=valor_parcela
            )
