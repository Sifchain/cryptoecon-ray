def get_reward_per_snapshot(**kwargs):
    """
    Get the global reward rate for each snapshot
    kwargs:
        miningSeconds: the period of the liquidity mining programme (in seconds)
        totalReward: total rewards to be distributed (in ROWAN)
        epochSeconds: the period of an epoch (in seconds) as we take a snapshot per epoch
    returns:
        rewardSnapshots: a list of number of rewards (in ROWAN) to be distributed for each snapshot
    """
    constants = {'miningSeconds':121*86400, # 121 days
                 'totalReward':30e6, # 30M
                 'epochSeconds':200*60, # 200 minutes
                 'multiplierSeconds': 121*86400, # 121 days
                 'multiplierBand': [1,4], # from 1x to 4x
                 'isGeyser': True} # Geyser or not    
    
    miningSeconds, totalReward, epochSeconds = kwargs['miningSeconds'], kwargs['totalReward'], kwargs['epochSeconds']
    maxSnapshotLength = int(miningSeconds/epochSeconds) # round down

    # a bodge to alleviate the inequality in reward distribution caused by sudden spike in liquidity add
    if isValidator:
        assert epochSeconds == 200*60, 'This bodge only works when epochSeconds == 200*60'
        liquidityWeightQuantized = [0,1,2,3,4,5]
        liquidityWeightSnapshotIndex = [0,60,88,119,270,372,maxSnapshotLength]
    else:
        assert epochSeconds == 200*60, 'This bodge only works when epochSeconds == 200*60'
        liquidityWeightQuantized = [0,1,4,5]
        liquidityWeightSnapshotIndex = [0,40,44,71,maxSnapshotLength]

    assert len(liquidityWeightQuantized)+1 == len(liquidityWeightSnapshotIndex), 'liquidityWeightQuantized or liquidityWeightSnapshotIndex is invalid'
    rewardSnapshots = []
    for weight, lowerlim, upperlim in zip(liquidityWeightQuantized, liquidityWeightSnapshotIndex[:-1], liquidityWeightSnapshotIndex[1:]):
        rewardSnapshots.extend([weight] * (upperlim-lowerlim))
    rewardSnapshots = [r/sum(rewardSnapshots)*totalReward for r in rewardSnapshots] # normalise
    return rewardSnapshots

# globalSnapshots = elementwisesum(list_userSnapshots)
# assert len(userSnapshots) == len(globalSnapshots), 'Lists have different lengths'

# rewardSnapshots = get_reward_per_snapshot(**kwargs)
# rewardSnapshots = rewardSnapshots[:len(userSnapshots)] # trim to ignore reward allocation for future snapshots
# userAccReward = sum([userStaked / globalStaked * reward if globalStaked > 0 else 0 for userStaked, globalStaked, reward in zip(userSnapshots, globalSnapshots, rewardSnapshots)])
# return userAccReward
