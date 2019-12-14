def parse_pose(context, snapshot):
    print('translation:', snapshot.pose.translation)
    print('rotation:', snapshot.pose.rotation)

parse_pose.field = 'pose'