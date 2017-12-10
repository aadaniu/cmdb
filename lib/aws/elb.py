# -*- coding: utf-8 -*-
# 2017-12-08
# by why

from lib.aws.aws import Aws
import json

class Elb(Aws):
    def __init__(self, *args, **kwargs):
        super(Elb, self).__init__(client_name="elb", *args, **kwargs)
        self._elb_list = []

    def get_elb(self):
        self._set_elb()
        return self._elb_list

    def _set_elb(self):
        self._elb_list = []
        response = self.client.describe_load_balancers()
        assert "LoadBalancerDescriptions" in response.keys()
        LoadBalancer = response["LoadBalancerDescriptions"]
        for lb in LoadBalancer:
            self._elb_list.append(
                {
                    "name": lb["LoadBalancerName"],
                    "Instances": lb["Instances"]
                }
            )


if __name__ == '__main__':
    e = Elb()
    print e.get_elb()