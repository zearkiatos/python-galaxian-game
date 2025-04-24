from typing import List


class CAnimation:
    def __init__(self, animations: dict) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = []
        for animation in animations["list"]:
            animation_data = AnimationData(
                animation["name"],
                animation["start"],
                animation["end"],
                animation["framerate"]
            )
            self.animations_list.append(animation_data)
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate

def set_animation(c_animation: CAnimation, animation_number: int):
    if c_animation.current_animation == animation_number:
        return

    c_animation.current_animation = animation_number
    c_animation.current_animation_time = 0

    c_animation.current_frame = c_animation.current_frame = c_animation.animations_list[
        c_animation.current_animation].start
