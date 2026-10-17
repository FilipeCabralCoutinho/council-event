from enrollments.models import Inscricoes
from .models import Participante


class PlenaryService:
    def create_new_participants(self):
        """
        Creates new participant records for all confirmed enrollments.
        """
        confirmed_participants = Inscricoes.objects.filter(
            status_pagamento='CONFIRMADO'
        )

        for participant in confirmed_participants:
            id_enrollment = participant.ids
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
        enrollment = Inscricoes.objects.filter(id=enrollment_id).first()
        if not enrollment:
            return None

        if enrollment.status_pagamento != 'CONFIRMADO':
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
