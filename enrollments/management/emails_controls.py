from enrollments.models import EmailControl, Inscricoes
from enrollments.services import Services
from enrollments.logging import logger
import time


class EmailReSender:
    def __init__(self):
        self.service = Services()

    def resend_failed_emails(self):
        failed_emails = EmailControl.objects.filter(status=False)
        
        logger.warning(f"Finded {failed_emails.count()} failed emails.")

        for email_log in failed_emails:
            time.sleep(5)

            try:
                enrollment = Inscricoes.objects.get(id=email_log.enrollment_id)
                logger.warning(f"Resending email {email_log.id}.")
                self.service.send_email(enrollment, email_log.email_type)
                email_log.delete()
            except Inscricoes.DoesNotExist:
                logger.error(f"Inscrição {email_log.enrollment_id} não encontrada. Deletando log de e-mail órfão.")
                email_log.delete()
            except Exception as e:
                logger.error(f"Error resending email {email_log.id}: {str(e)}", exc_info=True)
