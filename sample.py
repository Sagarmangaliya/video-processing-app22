import argparse
from video_generator import VideoGenerator
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx


def generate_segment(config, seed=None):
    """
    Generate one segment of video based on a config file and optional seed.
    """
    generator = VideoGenerator(config, seed=seed)
    frames = generator.forward()
    return generator.save_video(frames)


def stitch_segments(segments, output_path):
    """
    Concatenate list of video file paths into one video.
    """
    clips = [VideoFileClip(path) for path in segments]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=24, codec="libx264")
    return output_path


def add_audio(video_path, audio_path, output_path):
    """
    Overlay audio onto the video, looping audio if shorter than video.
    """
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    if audio.duration < video.duration:
        audio = audio.fx(vfx.loop, duration=video.duration)
    result = video.set_audio(audio)
    result.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate realistic video and optionally add audio.")
    parser.add_argument("--configs", nargs='+', required=True, help="Config TOML files for each segment.")
    parser.add_argument("--seeds", nargs='+', type=int, help="Seeds corresponding to each config.")
    parser.add_argument("--audio", type=str, help="Path to audio file to overlay.")
    parser.add_argument("--output", type=str, default="final.mp4", help="Output video path.")
    args = parser.parse_args()

    segment_paths = []
    for i, cfg in enumerate(args.configs):
        seed = args.seeds[i] if args.seeds and i < len(args.seeds) else None
        seg_path = f"segment_{i}.mp4"
        print(f"Generating segment {i} from {cfg} (seed={seed})...")
        generate_segment(cfg, seed)
        segment_paths.append(seg_path)

    stitched = "stitched.mp4"
    print("Stitching segments...")
    stitch_segments(segment_paths, stitched)

    if args.audio:
        print(f"Adding audio {args.audio}...")
        add_audio(stitched, args.audio, args.output)
    else:
        print(f"No audio specified, saving stitched video to {args.output}")
        import os; os.rename(stitched, args.output)

    print(f"Video ready: {args.output}")

if __name__ == "__main__":
    main()
