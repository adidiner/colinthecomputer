from colinthecomputer.protocol import (User,
                                       Snapshot,
                                       Pose,
                                       ColorImage,
                                       DepthImage,
                                       Feelings)


_USER_ID = 49
_USERNAME = 'Adi Dinerstein'
_BIRTH_TIMESTAMP = 974239200
_GENDER = 1

_COLOR_IMAGE = ColorImage(width=10,
                          height=20,
                          data=b'0'*20*10*3)
_DEPTH_IMAGE = DepthImage(width=5,
                          height=7,
                          data=[6.409690556097303e-10 for _ in range(35)])
_POSE1 = Pose(translation=Pose.Translation(x=1.0, y=2.0, z=3.0),
              rotation=Pose.Rotation(x=1.0, y=2.0, z=3.0, w=4.0))
_POSE2 = Pose(translation=Pose.Translation(x=0.5, y=3.0, z=4.0),
              rotation=Pose.Rotation(x=3.0, y=3.0, z=3.0, w=3.0))
_FEELINGS1 = Feelings(hunger=-0.5,
                      thirst=-0.125,
                      exhaustion=-0.5,
                      happiness=0.5)
_FEELINGS2 = Feelings(hunger=0.5,
                      thirst=0.125,
                      exhaustion=1.0,
                      happiness=-0.5)
_SNAPSHOT1 = Snapshot(datetime=1576237612000,
                      pose=_POSE1,
                      color_image=_COLOR_IMAGE,
                      depth_image=_DEPTH_IMAGE,
                      feelings=_FEELINGS1)
_SNAPSHOT2 = Snapshot(datetime=1576237618000,
                      pose=_POSE2,
                      color_image=_COLOR_IMAGE,
                      depth_image=_DEPTH_IMAGE,
                      feelings=_FEELINGS2)


SAMPLE = 'test_sample.mind'
USER = User(user_id=_USER_ID,
            username=_USERNAME,
            birthday=974239200,
            gender=_GENDER)
SNAPSHOTS = [_SNAPSHOT1, _SNAPSHOT2]

USER_JSON = '{"user_id": "49", ' \
            '"username": "Adi Dinerstein", ' \
            '"birthday": 974239200, ' \
            '"gender": "f"}'
SNAPSHOTS_JSON = ['{"datetime": "1576237612000", '
                  '"pose": {"translation": {"x": 1.0, "y": 2.0, "z": 3.0}, '
                           '"rotation": {"x": 1.0, "y": 2.0, "z": 3.0, "w": 4.0}}, '
                  '"color_image": '
                    '{"width": 10, '
                    '"height": 20, '
                    '"data": "tmpdir/49_1576237612000_color_image"}, '
                  '"depth_image": '
                    '{"width": 5, '
                    '"height": 7, '
                    '"data": "tmpdir/49_1576237612000_depth_image.npy"}, '
                  '"feelings": '
                    '{"hunger": -0.5, "thirst": -0.125, "exhaustion": -0.5, "happiness": 0.5}, '
                  '"user_id": 49}',
                  '{"datetime": "1576237618000", '
                  '"pose": {"translation": {"x": 0.5, "y": 3.0, "z": 4.0}, '
                           '"rotation": {"x": 3.0, "y": 3.0, "z": 3.0, "w": 3.0}}, '
                  '"color_image": '
                    '{"width": 10, '
                    '"height": 20, '
                    '"data": "tmpdir/raw_data_49_1576237618000_color_image"}, '
                  '"depth_image": '
                    '{"width": 5, '
                    '"height": 7, '
                    '"data": "tmpdir/taw_data_49_1576237618000_depth_image.npy"}, '
                  '"feelings": '
                    '{"hunger": 0.5, "thirst": 0.125, "exhaustion": 1.0, "happiness": -0.5}, '
                  '"user_id": 49}']

POSE_JSON = ['{"datetime": "1576237612000", "user_id": 49, '
             '"data": {"translation": {"x": 1.0, "y": 2.0, "z": 3.0}, '
                      '"rotation": {"x": 1.0, "y": 2.0, "z": 3.0, "w": 4.0}}}',
             '{"datetime": "1576237618000", "user_id": 49, '
             '"data": {"translation": {"x": 0.5, "y": 3.0, "z": 4.0}, '
             '"rotation": {"x": 3.0, "y": 3.0, "z": 3.0, "w": 3.0}}}']
COLOR_IMAGE_JSON = ['{"datetime": "1576237612000", "user_id": 49, '
                    '"data": {"path": "tmpdir/tesults_49_1576237612000_color_image.jpg"}}',
                    '{"datetime": "1576237618000", "user_id": 49, '
                    '"data": {"path": "tmpdir/results_49_1576237618000_color_image.jpg"}}']
DEPTH_IMAGE_JSON = ['{"datetime": "1576237612000", "user_id": 49, '
                    '"data": {"path": "tmpdir/results_49_1576237612000_depth_image.jpg"}}',
                    '{"datetime": "1576237618000", "user_id": 49, '
                    '"data": {"path": "tmpdir/results_49_1576237618000_depth_image.jpg"}}']
FEELINGS_JSON = ['{"datetime": "1576237612000", "user_id": 49, '
                 '"data": {"hunger": -0.5, "thirst": -0.125, "exhaustion": -0.5, "happiness": 0.5}}',
                 '{"datetime": "1576237618000", "user_id": 49, '
                 '"data": {"hunger": 0.5, "thirst": 0.125, "exhaustion": 1.0, "happiness": -0.5}}']
