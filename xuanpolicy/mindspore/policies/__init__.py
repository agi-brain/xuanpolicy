from gym.spaces import Space, Box, Discrete, Dict
import copy

from .categorical import ActorCriticPolicy as Categorical_AC_Policy
from .categorical import ActorPolicy as Categorical_Actor_Policy
from .categorical import PPGActorCritic as Categorical_PPG_Policy
from .categorical import SACDISPolicy

from .gaussian import ActorCriticPolicy as Gaussian_AC_Policy
from .gaussian import ActorPolicy as Gaussian_Actor_Policy
from .gaussian import SACPolicy as Gaussian_SAC_Policy
from .deterministic import BasicQnetwork, DuelQnetwork, NoisyQnetwork, C51Qnetwork, QRDQN_Network, DDPGPolicy, TD3Policy, CDQNPolicy, LDQNPolicy, \
     CLDQNPolicy, PDQNPolicy, MPDQNPolicy, SPDQNPolicy

from .mixers import *
from .deterministic_marl import BasicQnetwork as BasicQnetwork_marl
from .deterministic_marl import Basic_DDPG_policy as BasicDDPG_marl
from .deterministic_marl import MFQnetwork, MixingQnetwork, Weighted_MixingQnetwork, Qtran_MixingQnetwork, DCG_policy, \
    Basic_DDPG_policy, MADDPG_policy, MATD3_policy
from .categorical_marl import MultiAgentActorCriticPolicy, MeanFieldActorCriticPolicy, COMAPolicy
from .categorical_marl import MAPPO_ActorCriticPolicy as Categotical_MAPPO
from .gaussian_marl import Basic_ISAC_policy as Gaussian_ISAC
from .gaussian_marl import MASAC_policy as Gaussian_MASAC

Mixer = {
    "VDN": VDN_mixer,
    "QMIX": QMIX_mixer,
    "WQMIX": QMIX_FF_mixer,
    "QTRAN_alt": QTRAN_alt,
    "QTRAN_base": QTRAN_base
}

REGISTRY = {
    # ↓ Single-Agent DRL ↓ #
    "Categorical_AC": Categorical_AC_Policy,
    "Categorical_Actor": Categorical_Actor_Policy,
    "Categorical_PPG": Categorical_PPG_Policy,
    "Gaussian_AC": Gaussian_AC_Policy,
    "Gaussian_Actor": Gaussian_Actor_Policy,
    "Basic_Q_network": BasicQnetwork,
    "Duel_Q_network": DuelQnetwork,
    "Noisy_Q_network": NoisyQnetwork,
    "C51_Q_network": C51Qnetwork,
    "QR_Q_network": QRDQN_Network,
    "DDPG_Policy": DDPGPolicy,
    "Gaussian_SAC": Gaussian_SAC_Policy,
    "Discrete_SAC": SACDISPolicy,
    "TD3_Policy": TD3Policy,
    "CDQN_Policy": CDQNPolicy,
    "LDQN_Policy": LDQNPolicy,
    "CLDQN_Policy": CLDQNPolicy,
    "PDQN_Policy": PDQNPolicy,
    "MPDQN_Policy": MPDQNPolicy,
    "SPDQN_Policy": SPDQNPolicy,
    # ↓ Multi-Agent DRL ↓ #
    "Basic_Q_network_marl": BasicQnetwork_marl,
    "Mixing_Q_network": MixingQnetwork,
    "Weighted_Mixing_Q_network": Weighted_MixingQnetwork,
    "Qtran_Mixing_Q_network": Qtran_MixingQnetwork,
    "DCG_policy": DCG_policy,
    "Categorical_MAAC_policy": MultiAgentActorCriticPolicy,
    "Categorical_COMA_policy": COMAPolicy,
    "Independent_DDPG_policy": BasicDDPG_marl,
    "MADDPG_policy": MADDPG_policy,
    "MF_Q_network": MFQnetwork,
    "Categorical_MFAC_policy": MeanFieldActorCriticPolicy,
    "Categorical_MAPPO_policy": Categotical_MAPPO,
    "Gaussian_ISAC_policy": Gaussian_ISAC,
    "Gaussian_MASAC_policy": Gaussian_MASAC,
    "MATD3_policy": MATD3_policy
}

Policy_Inputs = {
    "Categorical_AC": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                       "normalize", "initialize", "activation"],
    "Categorical_Actor": ["action_space", "representation", "actor_hidden_size",
                          "normalize", "initialize", "activation"],
    "Categorical_PPG": ["action_space", "representation", "actor_hidden_size","critic_hidden_size",
                        "normalize", "initialize", "activation"],
    "Gaussian_AC": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                    "normalize", "initialize", "activation"],
    "Gaussian_SAC": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                     "initialize", "activation"],
    "Gaussian_Actor": ["action_space", "representation", "actor_hidden_size",
                       "normalize", "initialize", "activation"],
    "Basic_Q_network": ["action_space", "representation", "hidden_sizes",
                        "normalize", "initialize", "activation"],
    "Duel_Q_network": ["action_space", "representation", "hidden_sizes",
                       "normalize", "initialize", "activation"],
    "Noisy_Q_network": ["action_space", "representation", "hidden_sizes",
                       "normalize", "initialize", "activation"],
    "C51_Q_network": ["action_space", "atom_num","vmin", "vmax", "representation", "hidden_sizes",
                       "normalize", "initialize", "activation"],
    "QR_Q_network": ["action_space", "quantile_num", "representation", "hidden_sizes",
                       "normalize", "initialize", "activation"],
    "DDPG_Policy": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                    "initialize", "activation"],
    "Discrete_SAC": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                     "normalize", "initialize", "activation"],
    "TD3_Policy": ["action_space", "representation", "actor_hidden_size", "critic_hidden_size",
                   "normalize", "initialize", "activation"],
    "CDQN_Policy": ["action_space", "representation", "hidden_sizes",
                    "normalize", "initialize", "activation"],
    "LDQN_Policy": ["action_space", "representation", "hidden_sizes",
                    "normalize", "initialize", "activation"],
    "CLDQN_Policy": ["action_space", "representation", "hidden_sizes",
                    "normalize", "initialize", "activation"],
    "PDQN_Policy": ["observation_space", "action_space", "representation", "conactor_hidden_size",
                    "qnetwork_hidden_size", "normalize", "initialize", "activation"],
    "MPDQN_Policy": ['observation_space', 'action_space', 'representation', 'conactor_hidden_size',
                     'qnetwork_hidden_size', 'normalize', 'initialize', 'activation'],
    "SPDQN_Policy": ['observation_space', 'action_space', 'representation', 'conactor_hidden_size',
                     'qnetwork_hidden_size', 'normalize', 'initialize', 'activation'],
#  MARL policies  #
    "Basic_Q_network_marl": ["action_space", "n_agents", "representation", "hidden_sizes",
                             "normalize", "initialize", "activation"],
    "Mixing_Q_network": ["action_space", "n_agents", "representation", "mixer", "hidden_sizes",
                         "normalize", "initialize", "activation"],
    "Weighted_Mixing_Q_network": ["action_space", "n_agents", "representation", "mixer", "ff_mixer", "hidden_sizes",
                                  "normalize", "initialize", "activation"],
    "Qtran_Mixing_Q_network": ["action_space", "n_agents", "representation", "mixer", "qtran_mixer", "hidden_sizes",
                               "normalize", "initialize", "activation"],
    "Categorical_MAAC_policy": ["action_space", "n_agents", "representation", "mixer", "actor_hidden_size",
                                "critic_hidden_size", "normalize", "initialize", "activation"],
    "Categorical_MAPPO_policy": ["state_dim", "action_space", "n_agents", "representation", "actor_hidden_size",
                                "critic_hidden_size", "normalize", "initialize", "activation"],
    "Categorical_MFAC_policy": ["action_space", "n_agents", "representation", "actor_hidden_size",
                                "critic_hidden_size", "normalize", "initialize", "activation"],
    "Categorical_COMA_policy": ["state_dim", "action_space", "n_agents", "representation", "actor_hidden_size",
                                "critic_hidden_size", "normalize", "initialize", "activation"],
    "Independent_DDPG_policy": ["action_space", "n_agents", "representation", "actor_hidden_size",
                                "critic_hidden_size", "normalize", "initialize", "activation"],
    "MADDPG_policy": ["action_space", "n_agents", "representation", "actor_hidden_size", "critic_hidden_size",
                      "normalize", "initialize", "activation"],
    "MF_Q_network": ["action_space", "n_agents", "representation", "hidden_sizes",
                     "normalize", "initialize", "activation"],
    "Gaussian_ISAC_policy": ["action_space", "n_agents", "representation", "actor_hidden_size",
                             "critic_hidden_size", "normalize", "initialize", "activation"],
    "Gaussian_MASAC_policy": ["action_space", "n_agents", "representation", "actor_hidden_size", "critic_hidden_size",
                              "normalize", "initialize", "activation"],
    "MATD3_policy": ["action_space", "n_agents", "representation", "actor_hidden_size", "critic_hidden_size",
                     "normalize", "initialize", "activation"],
}

Policy_Inputs_All = {
    "state_dim": None,
    "action_space": None,
    "n_agents": None,
    "representation": None,
    "mixer": None,
    "ff_mixer": None,
    "qtran_mixer": None,
    "hidden_sizes": None,
    "actor_hidden_size": None,
    "critic_hidden_size": None,
    "normalize": None,
    "initialize": None,
    "activation": None,
    "fixed_std": None
}
