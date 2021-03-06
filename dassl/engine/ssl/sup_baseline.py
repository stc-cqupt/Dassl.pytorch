from torch.nn import functional as F

from dassl.engine import TRAINER_REGISTRY, TrainerXU
from dassl.metrics import compute_accuracy


@TRAINER_REGISTRY.register()
class SupBaseline(TrainerXU):
    """Supervised Baseline."""

    def forward_backward(self, batch_x, batch_u):
        input, label = self.parse_batch_train(batch_x, batch_u)
        output = self.model(input)
        loss = F.cross_entropy(output, label)
        self.model_backward_and_update(loss)

        output_dict = {
            'loss': loss.item(),
            'acc': compute_accuracy(output.detach(), label)[0].item(),
            'lr': self.optim.param_groups[0]['lr']
        }

        if (self.batch_idx + 1) == self.num_batches:
            self.update_lr()

        return output_dict

    def parse_batch_train(self, batch_x, batch_u):
        input = batch_x['img']
        label = batch_x['label']
        input = input.to(self.device)
        label = label.to(self.device)
        return input, label
