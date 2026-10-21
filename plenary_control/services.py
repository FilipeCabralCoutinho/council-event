from enrollments.models import Inscricoes
from .models import Participante


class PlenaryService:
    def create_all_participants(self):
        """
        Creates participant records based on all existing registrations.
        """
        enrollments = Inscricoes.objects.all()

        for participant in enrollments:

            # verifica se o participante já existe no banco de dados
            id_enrollment = participant.id
            participant_exists = Participante.objects.filter(
                id_inscricao=id_enrollment
            ).first()

            if not participant_exists:
                new_participant = Participante(
                    id_inscricao=id_enrollment,
                    nome=participant.nome,
                    email=participant.email,
                    whatsapp=participant.whatsapp,
                    cpf=participant.cpf,
                    status_pagamento=participant.status_pagamento,
                    distrito=participant.distrito,
                    igreja=participant.igreja,
                    funcao=participant.funcao,
                    pernoite=participant.pernoite,
                    comorbidade=participant.possui_comorbidade,
                    qual_comorbidade=participant.qual_comorbidade
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
            qual_comorbidade=enrollment.qual_comorbidade
        )

        new_participant.save()

        return new_participant

    def get_all_participants(self):
        """
        Retrieves all participant records.
        """
        return Participante.objects.all()
