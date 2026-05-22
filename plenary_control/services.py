from ..enrollments.models import Inscricoes
from .models import Participantes


class PlenaryControlService:
    def create_new_participants(self):
        """
        Creates new participant records for all confirmed enrollments.
        """
        confirmed_participants = Inscricoes.objects.filter(
            status_pagamento='CONFIRMADO'
        )

        for participant in confirmed_participants:
            id_enrollment = participant.id_inscricao
            check_participant = Participantes.objects.filter(
                id_inscricao=id_enrollment
            ).first()

            if not check_participant:
                new_participant = Participantes(
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
                    comorbidade=participant.comorbidade,
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

        new_participant = Participantes(
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
