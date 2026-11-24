from enrollments.models import Inscricoes
from .models import Participante
import pandas as pd
import io
from django.http import HttpResponse
from .logging import setup_logging
from pathlib import Path
from django.utils import timezone

logger = setup_logging()


class PlenaryService:
    def create_all_participants(self):
        """
        Creates participant records based on all existing registrations.
        """
        logger.info("create_all_participants method initialized.")

        enrollments = Inscricoes.objects.all()

        for enrollment in enrollments:

            # verifica se o participante já existe no banco de dados
            id_enrollment = enrollment.id
            participant_exists = Participante.objects.filter(
                id_inscricao=id_enrollment
            ).first()

            if not participant_exists:
                new_participant = Participante(
                    id_inscricao=id_enrollment,
                    nome=enrollment.nome,
                    email=enrollment.email,
                    whatsapp=enrollment.whatsapp,
                    cpf=enrollment.cpf,
                    status_pagamento=enrollment.status_pagamento,
                    distrito=enrollment.distrito,
                    igreja=enrollment.igreja,
                    funcao=enrollment.funcao,
                    pernoite=enrollment.pernoite,
                    comorbidade=enrollment.possui_comorbidade,
                    qual_comorbidade=enrollment.qual_comorbidade,
                    sexo=enrollment.sexo
                )
                new_participant.save()

        logger.info("create_all_participants method completed successfully!")

        return True

    def create_participant(self, enrollment_id):
        """
        Creates a new participant record based on the enrollment ID.
        """
        # verifica se a inscrição existe e a guarda na variável
        logger.info("create_participant method initialized.")

        enrollment = Inscricoes.objects.filter(id=enrollment_id).first()
        if not enrollment:
            return None

        new_participant = Participante(
            id_inscricao=enrollment.id,
            nome=enrollment.nome,
            email=enrollment.email,
            whatsapp=enrollment.whatsapp,
            cpf=enrollment.cpf,
            status_pagamento=enrollment.status_pagamento,
            distrito=enrollment.distrito,
            igreja=enrollment.igreja,
            funcao=enrollment.funcao,
            pernoite=enrollment.pernoite,
            comorbidade=enrollment.possui_comorbidade,
            qual_comorbidade=enrollment.qual_comorbidade,
            sexo=enrollment.sexo
        )

        new_participant.save()

        logger.info("create_participant method completed successfully!")

        return new_participant

    def update_participant(self, enrollment_id):
        """
        Updates an existing participant record based on the enrollment ID.
        """
        logger.info("update_participant method initialized.")

        enrollment = Inscricoes.objects.filter(id=enrollment_id).first()
        if not enrollment:
            return None

        participant = Participante.objects.filter(id_inscricao=enrollment.id).first()
        if not participant:
            return None

        participant.nome = enrollment.nome
        participant.email = enrollment.email
        participant.whatsapp = enrollment.whatsapp
        participant.cpf = enrollment.cpf
        participant.status_pagamento = enrollment.status_pagamento
        participant.distrito = enrollment.distrito.nome
        participant.igreja = enrollment.igreja.nome
        participant.funcao = enrollment.funcao
        participant.pernoite = enrollment.pernoite
        participant.comorbidade = enrollment.possui_comorbidade
        participant.qual_comorbidade = enrollment.qual_comorbidade
        participant.sexo = enrollment.sexo

        participant.save()

        logger.info("update_participant method completed successfully!")

        return participant

    def delete_participant(self, enrollment_id):
        """
        Deletes a participant record based on the enrollment ID.
        """
        logger.info("delete_participant method initialized.")

        participant = Participante.objects.filter(id_inscricao=enrollment_id).first()
        if not participant:
            return None

        participant.delete()

        logger.info("delete_participant method completed successfully!")

        return True

    def get_all_participants(self):
        """
        Retrieves all participant records.
        """
        logger.info("get_all_participants method in process.")
        return Participante.objects.all()

    def export_participants_to_excel(self):
        logger.info("export_participants_to_excel method initialized.")

        output = self.create_excel_relatory_participants()

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="participantes_concilio.xlsx"'

        logger.info("Excel spreadsheet generated successfully!")

        return response

    def create_excel_relatory_participants(self):
        logger.info("create_excel_relatory_participants method initialized.")
        participants = Participante.objects.order_by("id_participante")

        data = []

        for i in participants:
            data.append(
                {
                    "ID_Participante": i.id_participante,
                    "ID_Inscricao": i.id_inscricao,
                    "Nome": i.nome,
                    "Celular": i.whatsapp,
                    "Distrito": i.distrito,
                    "Igreja": i.igreja,
                    "Função": i.funcao,
                    "Vai Dormir no Efraim?": i.pernoite,
                    "Sexo": i.sexo,
                    "No Plenário?": i.no_plenario,
                }
            )

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Participantes')

        output.seek(0)
        return output

    def save_backup_excel(self):
        logger.info("save_backup_excel method initialized.")

        data = self.create_excel_relatory_participants()

        # Obtém o diretório atual do arquivo
        current_dir = Path(__file__).resolve().parent

        # Define o caminho para a pasta de backups
        backups_dir = current_dir / "backups"

        # Cria a pasta de backups se ela não existir
        backups_dir.mkdir(exist_ok=True)

        # Gera um nome de arquivo único com base na data e hora atuais
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"backup_participantes_{timestamp}.xlsx"
        # Define o caminho completo do arquivo de backup
        file_path = backups_dir / file_name

        # Salva os dados gerados pelo relatório em disco
        file_path.write_bytes(data.getvalue())

        logger.info("Excel backup saved successfully: %s", file_path)

        return file_path
