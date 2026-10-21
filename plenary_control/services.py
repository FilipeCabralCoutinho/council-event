from enrollments.models import Inscricoes
from .models import Participante
import pandas as pd
import io
from django.http import HttpResponse


class PlenaryService:
    def create_all_participants(self):
        """
        Creates participant records based on all existing registrations.
        """
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

        return True

    def create_participant(self, enrollment_id):
        """
        Creates a new participant record based on the enrollment ID.
        """
        # verifica se a inscrição existe e a guarda na variável
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

        return new_participant

    def get_all_participants(self):
        """
        Retrieves all participant records.
        """
        return Participante.objects.all()

    @staticmethod
    def export_participants_to_excel(self):
        #logger.info("export_participants_to_excel method initialized.")

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

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="participantes_concilio.xlsx"'

        #logger.info("Excel spreadsheet generated successfully!")

        return response
