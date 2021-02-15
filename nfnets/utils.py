import torch
from torch import nn

from nfnets import WSConv2d


def replace_conv(module: nn.Module):
    """Recursively replaces every convolution with WSConv2d.

    Usage: replace_conv(model) #(In-line replacement)
    Args:
      module(nn.Module): target's model whose convolutions must be replaced.
    """
    for name, mod in module.named_children():
        target_mod = getattr(module, name)
        if type(mod) == torch.nn.Conv2d:
            setattr(module, name, WSConv2d(target_mod.in_channels, target_mod.out_channels, target_mod.kernel_size,
                                           target_mod.stride, target_mod.padding, target_mod.dilation, target_mod.groups, target_mod.bias))
        
        if type(mod) == torch.nn.BatchNorm2d:
            setattr(module, name, torch.nn.Identity())

    for name, mod in module.named_children():
        replace_conv(mod)
