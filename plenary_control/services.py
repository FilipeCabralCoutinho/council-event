from ..enrollments.models import Inscricoes
from .models import Participantes


class PlenaryControlService:
    def get_all_confirmed_enrollments(self):
        return Inscricoes.objects.filter(status_pagamento='CONFIRMADO')

    def create_new_participants(self):
        confirmed_participants = self.get_all_confirmed_enrollments()

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
