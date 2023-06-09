'''
Repo: XuanPolicy

Example for single agent DRL:
$ python main.py --agent-name dqn --env-name toy_env/CartPole-v0

'''
import argparse
from xuanpolicy import get_runner


def parse_args():
    parser = argparse.ArgumentParser("Multi-Agent Reinforcement Learning With Causality Detection.")
    parser.add_argument("--agent-name", type=str, default="dqn")
    parser.add_argument("--env-name", type=str, default="toy_env/CartPole-v0")
    parser.add_argument("--test", type=int, default=0)
    return parser.parse_args()


if __name__ == '__main__':
    parser = parse_args()
    runner = get_runner(agent_name=parser.agent_name,
                        env_name=parser.env_name,
                        parser_args=parser,
                        is_test=parser.test)
    runner.run()
