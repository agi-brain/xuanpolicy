"""
Value Decomposition Networks (VDN)
Paper link:
https://arxiv.org/pdf/1706.05296.pdf
Implementation: Pytorch
"""
from xuanpolicy.torch.learners import *


class VDN_Learner(LearnerMAS):
    def __init__(self,
                 config: Namespace,
                 policy: nn.Module,
                 optimizer: torch.optim.Optimizer,
                 scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
                 device: Optional[Union[int, str, torch.device]] = None,
                 modeldir: str = "./",
                 gamma: float = 0.99,
                 sync_frequency: int = 100
                 ):
        self.gamma = gamma
        self.sync_frequency = sync_frequency
        self.use_recurrent = config.use_recurrent
        self.mse_loss = nn.MSELoss()
        super(VDN_Learner, self).__init__(config, policy, optimizer, scheduler, device, modeldir)

    def update(self, sample):
        self.iterations += 1
        obs = torch.Tensor(sample['obs']).to(self.device)
        actions = torch.Tensor(sample['actions']).to(self.device)
        obs_next = torch.Tensor(sample['obs_next']).to(self.device)
        rewards = torch.Tensor(sample['rewards']).mean(dim=1).to(self.device)
        terminals = torch.Tensor(sample['terminals']).all(dim=1, keepdims=True).float().to(self.device)
        agent_mask = torch.Tensor(sample['agent_mask']).float().view(-1, self.n_agents, 1).to(self.device)
        IDs = torch.eye(self.n_agents).unsqueeze(0).expand(self.args.batch_size, -1, -1).to(self.device)
        batch_size = actions.shape[0]

        rnn_hidden = self.policy.representation.init_hidden(batch_size) if self.use_recurrent else [None]
        _, _, q_eval = self.policy(obs, IDs, *rnn_hidden)
        q_eval_a = q_eval.gather(-1, actions.long().view([self.args.batch_size, self.n_agents, 1]))
        q_tot_eval = self.policy.Q_tot(q_eval_a * agent_mask)
        target_rnn_hidden = self.policy.target_representation.init_hidden(batch_size) if self.use_recurrent else [None]
        _, q_next = self.policy.target_Q(obs_next, IDs, *target_rnn_hidden)
        if self.args.double_q:
            _, action_next_greedy, _ = self.policy(obs_next, IDs)
            q_next_a = q_next.gather(-1, action_next_greedy.unsqueeze(-1).long().detach())
        else:
            q_next_a = q_next.max(dim=-1, keepdim=True).values
        q_tot_next = self.policy.target_Q_tot(q_next_a * agent_mask)
        q_tot_target = rewards + (1-terminals) * self.args.gamma * q_tot_next

        # calculate the loss function
        loss = self.mse_loss(q_tot_eval, q_tot_target.detach())
        self.optimizer.zero_grad()
        loss.backward()
        if self.args.use_grad_clip:
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.args.grad_clip_norm)
        self.optimizer.step()
        if self.scheduler is not None:
            self.scheduler.step()

        if self.iterations % self.sync_frequency == 0:
            self.policy.copy_target()
        lr = self.optimizer.state_dict()['param_groups'][0]['lr']

        info = {
            "learning_rate": lr,
            "loss_Q": loss.item(),
            "predictQ": q_tot_eval.mean().item()
        }

        return info

    def update_sc2(self, sample):
        self.iterations += 1
        obs = torch.Tensor(sample['obs']).to(self.device)
        actions = torch.Tensor(sample['actions']).to(self.device)
        obs_next = torch.Tensor(sample['obs_next']).to(self.device)
        rewards = torch.Tensor(sample['rewards']).mean(dim=1).to(self.device)
        terminals = torch.Tensor(sample['terminals']).all(dim=1, keepdims=True).float().to(self.device)
        agent_mask = torch.Tensor(sample['agent_mask']).float().view(-1, self.n_agents, 1).to(self.device)
        IDs = torch.eye(self.n_agents).unsqueeze(0).expand(self.args.batch_size, -1, -1).to(self.device)
        batch_size = actions.shape[0]

        rnn_hidden = self.policy.representation.init_hidden(batch_size) if self.use_recurrent else [None]
        _, _, q_eval = self.policy(obs, IDs, *rnn_hidden)
        q_eval_a = q_eval.gather(-1, actions.long().view([self.args.batch_size, self.n_agents, 1]))
        q_tot_eval = self.policy.Q_tot(q_eval_a * agent_mask)
        target_rnn_hidden = self.policy.target_representation.init_hidden(batch_size) if self.use_recurrent else [None]
        _, q_next = self.policy.target_Q(obs_next, IDs, *target_rnn_hidden)
        if self.args.double_q:
            _, action_next_greedy, _ = self.policy(obs_next, IDs)
            q_next_a = q_next.gather(-1, action_next_greedy.unsqueeze(-1).long().detach())
        else:
            q_next_a = q_next.max(dim=-1, keepdim=True).values
        q_tot_next = self.policy.target_Q_tot(q_next_a * agent_mask)
        q_tot_target = rewards + (1 - terminals) * self.args.gamma * q_tot_next

        # calculate the loss function
        loss = self.mse_loss(q_tot_eval, q_tot_target.detach())
        self.optimizer.zero_grad()
        loss.backward()
        if self.args.use_grad_clip:
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.args.grad_clip_norm)
        self.optimizer.step()
        if self.scheduler is not None:
            self.scheduler.step()

        if self.iterations % self.sync_frequency == 0:
            self.policy.copy_target()
        lr = self.optimizer.state_dict()['param_groups'][0]['lr']

        info = {
            "learning_rate": lr,
            "loss_Q": loss.item(),
            "predictQ": q_tot_eval.mean().item()
        }

        return info
