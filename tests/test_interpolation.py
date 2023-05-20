import math
from typing import Iterable

from hypothesis import given, strategies as st

from wpimath.geometry import Pose2d, Rotation2d
from wpimath.interpolation import (
    TimeInterpolatableFloatBuffer,
    TimeInterpolatablePose2dBuffer,
    TimeInterpolatableRotation2dBuffer,
)


def test_float():
    buffer = TimeInterpolatableFloatBuffer(10)

    buffer.addSample(0, 0)
    assert buffer.sample(0) == 0
    buffer.addSample(1, 1)
    assert buffer.sample(0.5) == 0.5
    assert buffer.sample(1) == 1
    buffer.addSample(3, 2)
    assert buffer.sample(2) == 1.5

    buffer.addSample(10.5, 2)
    assert buffer.sample(0) == 1


@given(
    st.builds(TimeInterpolatableFloatBuffer, st.floats(1, 10)),
    st.iterables(
        st.tuples(st.booleans(), st.floats(0, 100))
    ),
)
def test_float_arbitrary(
    buffer: TimeInterpolatableFloatBuffer, instructions: Iterable[tuple[bool, float]]
):
    for should_add, time_s in instructions:
        if should_add:
            buffer.addSample(time_s, 0)
        else:
            buffer.sample(time_s)


def test_rotation2d():
    buffer = TimeInterpolatableRotation2dBuffer(10)

    buffer.addSample(0, Rotation2d(0))
    assert buffer.sample(0) == Rotation2d(0)
    buffer.addSample(1, Rotation2d(1))
    assert buffer.sample(0.5) == Rotation2d(0.5)
    assert buffer.sample(1) == Rotation2d(1)
    buffer.addSample(3, Rotation2d(2))
    assert buffer.sample(2) == Rotation2d(1.5)

    buffer.addSample(10.5, Rotation2d(2))
    assert buffer.sample(0) == Rotation2d(1)


def test_pose2d():
    buffer = TimeInterpolatablePose2dBuffer(10)
    # We expect to be at (1 - 1/sqrt(2), 1/sqrt(2), 45deg) at t=0.5
    buffer.addSample(0, Pose2d(0, 0, Rotation2d.fromDegrees(90)))
    buffer.addSample(1, Pose2d(1, 1, Rotation2d(0)))
    sample = buffer.sample(0.5)
    assert math.isclose(sample.X(), 1 - 1 / 2**0.5)
    assert math.isclose(sample.Y(), 1 / 2**0.5)
    assert math.isclose(sample.rotation().degrees(), 45)
