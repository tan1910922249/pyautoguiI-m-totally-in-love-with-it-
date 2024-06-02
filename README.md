# pyautoguiI-m-totally-in-love-with-it-
I'm totally in love with it!
from moviepy.editor import VideoFileClip, concatenate_videoclips
import librosa
import numpy as np
import os

def get_audio_peaks(audio_file, sr=22050, threshold=0.05):
    y, sr = librosa.load(audio_file, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    # 寻找频谱的局部最大值（作为音频的峰值）
    peaks, _ = librosa.find_peaks(D, threshold=threshold)

    # 将帧索引转换为时间戳
    times = librosa.frames_to_time(peaks, sr=sr)
    return times

def calculate_speed_based_on_peak(peak_time, video_clip, base_speed=1.0, max_speed_increase=1.0):
    # 根据波峰的时间点获取视频中的相应片段
    peak_clip = video_clip.subclip(peak_time - 0.1, peak_time + 0.1)
    
    # 计算片段的原始持续时间
    original_duration = peak_clip.duration
    
    # 增加速度以缩短视频片段的持续时间
    speed_increase = min(max_speed_increase, peak_clip.duration / 0.2)  # 假设最短持续时间为0.2秒
    new_speed = base_speed + speed_increase
    peak_clip.set_speed(new_speed)
    
    # 更新片段的持续时间以匹配原始时长（通过增加速度缩短了时长）
    peak_clip = peak_clip.set_duration(original_duration)
    
    return peak_clip

def adjust_clip_speed_based_on_audio(video_clip, audio_file, sr=22050, threshold=0.05):
    times = get_audio_peaks(audio_file, sr=sr, threshold=threshold)
    
    # 初始化一个空的clips列表来存储按速度分割的视频片段
    clips = [video_clip.subclip(0, times[0]).set_speed(1.0)]  # 添加视频的开始部分，正常速度

    # 对于每个波峰，创建一个加速的片段
    for time in times:
        peak_clip = calculate_speed_based_on_peak(time, video_clip)
        clips.append(peak_clip)

    # 添加视频剩余的部分，正常速度
    if times and times[-1] < video_clip.duration:
        clips.append(video_clip.subclip(times[-1], video_clip.duration).set_speed(1.0))

    # 使用concatenate_videoclips连接所有片段
    final_clip = concatenate_videoclips(clips, method="compose")
    return final_clip

# 设置视频和音频文件夹路径
input_video_folder = 'D:\\视频\\视频剪辑\\源视频'
input_audio_folder = 'D:\\音频\\音频文件'

# 指定输出文件夹
output_folder = 'D:\\视频\\输出'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历所有视频文件
for video_file in os.listdir(input_video_folder):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(input_video_folder, video_file)
        audio_file = os.path.splitext(video_file)[0] + '.mp3'  # 假设音频文件名与视频文件名相同，只是扩展名不同
        audio_path = os.path.join(input_audio_folder, audio_file)
        
        # 加载视频和音频文件
        video_clip = VideoFileClip(video_path)
        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_path)
        
        # 构造输出文件名
        output_video_file = os.path.join(output_folder, os.path.splitext(video_file)[0] + '_speed_adjusted.mp4')
        
        # 写入调整速度后的视频文件
        adjusted_clip.write_videofile(output_video_file, codec='libx264')
        
        # 关闭打开的剪辑
        video_clip.close()
        adjusted_clip.close()

```python
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import os

# 其他函数（get_audio_peaks, calculate_speed_based_on_peak, adjust_clip_speed_based_on_audio）保持不变

def add_audio_to_video(video_clip, audio_clip):
    # 将音频剪辑与视频剪辑同步
    video_clip = video_clip.set_audio(audio_clip)
    return video_clip

# 假设你有一个包含视频文件的列表
input_video_folder = 'D:\\视频\\视频剪辑\\源视频'
input_audio_folder = 'D:\\音频\\音频文件'  # 音乐音频文件夹
video_files = [f for f in os.listdir(input_video_folder) if f.endswith('.mp4')]
video_clips = [VideoFileClip(os.path.join(input_video_folder, f)) for f in video_files]

# 对于每个视频剪辑，找到对应的音频文件并调整速度
final_clips = []
for video_clip in video_clips:
    video_filename = os.path.splitext(os.path.basename(video_clip.filepath))[0]
    audio_filename = video_filename + '.mp3'  # 假设音频文件名与视频文件名相同，只是扩展名不同
    audio_file_path = os.path.join(input_audio_folder, audio_filename)
    
    # 确保音频文件存在
    if not os.path.exists(audio_file_path):
        print(f"警告：音频文件 {audio_filename} 不存在，视频将使用默认无声。")
        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, None)
    else:
        # 加载音频文件
        audio_clip = AudioFileClip(audio_file_path)
        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_clip.filepath)
    
    # 将音频添加到调整速度后的视频
    final_clip = add_audio_to_video(adjusted_clip, audio_clip)
    
    # 存储最终剪辑
    final_clips.append(final_clip)

# 合并所有调整过速度并添加了音频的视频剪辑
final_concatenated_clip = concatenate_videoclips(final_clips, method="compose")

# 指定输出文件夹并创建
output_folder = 'D:\\视频\\输出'
os.makedirs(output_folder, exist_ok=True)

# 构造输出文件名
output_video_file = os.path.join(output_folder, 'final_output.mp4')

# 写入视频文件
final_concatenated_clip.write_videofile(output_video_file, codec='libx264')

# 关闭所有剪辑
for clip in final_clips:
    clip.close()
final_concatenated_clip.close()
```

# 示例：添加异常处理和文件存在性检查
def load_audio_clip(audio_file_path):
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件 {audio_file_path} 不存在。")
    return AudioFileClip(audio_file_path)

# 在主逻辑中使用
try:
    audio_clip = load_audio_clip(audio_file_path)
except FileNotFoundError as e:
    print(e)
    audio_clip = None  # 或者设置为默认无声

# 示例：使用命令行参数
import argparse

parser = argparse.ArgumentParser(description="视频速度调整工具")
parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
parser.add_argument("--output_folder", required=True, help="输出文件夹路径")

args = parser.parse_args()

# 使用args变量代替硬编码的路径
import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np

# 函数：加载音频剪辑，增加异常处理
def load_audio_clip(audio_file_path):
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件 {audio_file_path} 不存在。")
    return AudioFileClip(audio_file_path)

# 其他函数（get_audio_peaks, calculate_speed_based_on_peak, adjust_clip_speed_based_on_audio）保持不变

# 函数：添加音频到视频，并处理异常
def add_audio_to_video(video_clip, audio_clip):
    try:
        video_clip = video_clip.set_audio(audio_clip)
    except Exception as e:
        print(f"无法添加音频到视频：{e}")
    return video_clip

# 函数：处理单个视频文件
def process_video(video_path, audio_path, output_folder):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = load_audio_clip(audio_path)

        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_clip.filepath)
        final_clip = add_audio_to_video(adjusted_clip, audio_clip)

        output_video_file = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0] + '_speed_adjusted.mp4')
        final_clip.write_videofile(output_video_file, codec='libx264')

    except Exception as e:
        print(f"处理视频 {video_path} 时发生错误：{e}")
    finally:
        video_clip.close()
        if adjusted_clip is not final_clip:
            adjusted_clip.close()
        final_clip.close()

# 主逻辑
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    args = parser.parse_args()

    # 确保输出文件夹存在
    os.makedirs(args.output_folder, exist_ok=True)

    # 遍历所有视频文件
    video_files = [f for f in os.listdir(args.input_video_folder) if f.endswith('.mp4')]
    for video_file in video_files:
        video_path = os.path.join(args.input_video_folder, video_file)
        audio_file = os.path.splitext(video_file)[0] + '.mp3'
        audio_path = os.path.join(args.input_audio_folder, audio_file)
        
        process_video(video_path, audio_path, args.output_folder)
import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 其他函数（get_audio_peaks, calculate_speed_based_on_peak）保持不变

def adjust_clip_speed_based_on_audio(video_clip, audio_path, sr=22050, threshold=0.05):
    try:
        audio_clip = load_audio_clip(audio_path, sr)
    except FileNotFoundError as e:
        logging.error(e)
        audio_clip = None
    
    times = get_audio_peaks(audio_clip.filepath if audio_clip else None, sr, threshold)
    clips = [video_clip.subclip(0, times[0] if times else video_clip.duration).set_speed(1.0)]

    for time in times:
        peak_clip = calculate_speed_based_on_peak(time, video_clip)
        clips.append(peak_clip)

    if times and times[-1] < video_clip.duration:
        clips.append(video_clip.subclip(times[-1], video_clip.duration).set_speed(1.0))

    return concatenate_videoclips(clips, method="compose")

def process_video_file(video_file, input_audio_folder, output_folder, sr=22050, threshold=0.05):
    video_path = os.path.join(input_video_folder, video_file)
    audio_file = f"{os.path.splitext(video_file)[0]}.mp3"
    audio_path = os.path.join(input_audio_folder, audio_file)
    output_video_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}_speed_adjusted.mp4")

    try:
        with VideoFileClip(video_path) as video_clip:
            adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_path, sr, threshold)
            adjusted_clip.write_videofile(output_video_path, codec='libx264')
    except Exception as e:
        logging.error(f"处理视频 {video_path} 时发生错误：{e}")
    finally:
        if 'adjusted_clip' in locals():
            adjusted_clip.close()

def main(input_video_folder, input_audio_folder, output_folder, sr=22050, threshold=0.05):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    
    video_files = (f for f in os.listdir(input_video_folder) if f.endswith('.mp4'))
    for video_file in video_files:
        process_video_file(video_file, input_audio_folder, output_folder, sr, threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    parser.add_argument("--sr", type=int, default=22050, help="音频采样率")
    parser.add_argument("--threshold", type=float, default=0.05, help="音频峰值检测阈值")

    args = parser.parse_args()
    main(**vars(args))
    import os
import argparse
from moviepy.editor import VideoFileClip
import librosa
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# 假设其他函数（get_audio_peaks, calculate_speed_based_on_peak, adjust_clip_speed_based_on_audio）已定义

def process_video(args):
    video_path, audio_path, output_folder, sr, threshold = args
    try:
        video_clip = VideoFileClip(video_path)
        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_path, sr, threshold)
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_speed_adjusted.mp4")
        adjusted_clip.write_videofile(output_path, codec='libx264')
        print(f"Processed {video_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
    finally:
        if video_clip.is_opened:
            video_clip.close()
        if adjusted_clip.is_opened:
            adjusted_clip.close()

def main(input_video_folder, input_audio_folder, output_folder, sr=22050, threshold=0.05, max_workers=4):
    os.makedirs(output_folder, exist_ok=True)
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith('.mp4')]
    video_paths = [os.path.join(input_video_folder, video_file) for video_file in video_files]
    
    arguments = [
        (video_path, os.path.join(input_audio_folder, os.path.splitext(os.path.basename(video_path))[0] + '.mp3'),
         output_folder, sr, threshold) for video_path in video_paths
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_video = {executor.submit(process_video, args): args for args in arguments}
        for future in as_completed(future_to_video):
            video_path = future_to_video[future][0]
            try:
                future.result()
            except Exception as e:
                print(f"{video_path} generated an exception: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded video processing tool")
    parser.add_argument("--input_video_folder", required=True, help="Path to the input video folder")
    parser.add_argument("--input_audio_folder", required=True, help="Path to the input audio folder")
    parser.add_argument("--output_folder", required=True, help="Path to the output folder")
    parser.add_argument("--sr", type=int, default=22050, help="Sample rate for audio processing")
    parser.add_argument("--threshold", type=float, default=0.05, help="Threshold for audio peak detection")
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of worker threads")

    args = parser.parse_args()
    main(**vars(args))import os
import argparse
from moviepy.editor import VideoFileClip
import librosa
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 函数定义保持不变，这里只展示新增或修改的部分

def load_audio_clip(audio_file_path, sr=22050):
    y, sr = librosa.load(audio_file_path, sr=sr)
    return y, sr

def process_video_file(args):
    video_path, audio_file_path, output_folder, sr, threshold = args
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_video_file = os.path.join(output_folder, f"{video_filename}_speed_adjusted.mp4")

    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = load_audio_clip(audio_file_path, sr) if os.path.exists(audio_file_path) else None
        adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_clip, sr, threshold)
        
        adjusted_clip.write_videofile(output_video_file, codec='libx264')
        logging.info(f"视频 {video_path} 处理完成。")
    except Exception as e:
        logging.error(f"处理视频 {video_path} 时发生错误：{e}")
    finally:
        video_clip.close()
        if audio_clip:
            audio_clip.close()
        if adjusted_clip is not None:
            adjusted_clip.close()

def main(input_video_folder, input_audio_folder, output_folder, sr=22050, threshold=0.05, max_workers=4):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 收集所有视频文件的路径
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith('.mp4')]
    video_paths = [os.path.join(input_video_folder, f) for f in video_files]
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 为每个视频文件创建一个线程任务
        futures = [executor.submit(process_video_file, (video_path, 
                           os.path.join(input_audio_folder, os.path.splitext(os.path.basename(video_path))[0] + '.mp3'),
                           output_folder, sr, threshold)) for video_path in video_paths]
        
        # 等待所有任务完成
        for future in futures:
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    parser.add_argument("--sr", type=int, default=22050, help="音频采样率")
    parser.add_argument("--threshold", type=float, default=0.05, help="音频峰值检测阈值")
    parser.add_argument("--max_workers", type=int, default=4, help="最大线程数")

    args = parser.parse_args()
    main(**vars(args))
    import os
import logging

def process_video_file(video_path, audio_path, output_folder, min_segment_length=60, max_segment_length=300):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_clip = load_clip(video_path, 'video')
    audio_clip = load_clip(audio_path, 'audio')

    if not video_clip or not audio_clip:
        logging.error("视频或音频文件加载失败")
        return

    start_time = 0
    segment_count = 1
    times = get_audio_peaks(audio_clip.get_audio(), min_segment_length)

    while start_time < video_clip.duration:
        # 找到最近的音频波峰作为结束时间
        end_time = find_closest_peak(times, start_time + min_segment_length)
        end_time = min(end_time, video_clip.duration)
        
        if (end_time - start_time) < min_segment_length:
            # 如果片段太短，跳过这个波峰，找到下一个
            start_time = end_time
            continue

        if (end_time - start_time) > max_segment_length:
            # 如果片段太长，调整结束时间为最大长度
            end_time = start_time + max_segment_length

        segment_clip = video_clip.subclip(start_time, end_time)

        # 调整速度等操作
        # ...

        # 保存分段视频
        segment_filename = f"video_segment_{segment_count:03d}.mp4"
        segment_output_path = os.path.join(output_folder, segment_filename)
        segment_clip.write_videofile(segment_output_path, codec='libx264')
        logging.info(f"视频分段处理完成：{segment_output_path}")

        start_time = end_time
        segment_count += 1

    video_clip.close()
    audio_clip.close()

def get_audio_peaks(audio_data, min_segment_length):
    # 这里应该是一个函数，根据音频数据和最小片段长度返回音频波峰时间点列表
    # 需要您自己实现或提供这个函数的实现
    pass

def find_closest_peak(peaks, time):
    # 找到给定时间最近的波峰
    return min(peaks, key=lambda t: abs(t - time))

# 假设 load_clip 函数和其他必要的函数已经实现
def load_clip(path, media_type):
    # 根据文件路径和媒体类型加载媒体片段
    # 需要您自己实现或提供这个函数的实现
    pass

# 调用示例
video_path = 'path_to_your_video.mp4'
audio_path = 'path_to_your_audio.mp3'
output_folder = 'path_to_output_folder'
process_video_file(video_path, audio_path, output_folder)   
def process_video_file(video_path, audio_path, output_folder, max_segment_length=10):
    video_clip = load_clip(video_path, 'video')
    audio_clip = load_clip(audio_path, 'audio')

    if not video_clip or not audio_clip:
        return

    start_time = 0
    segment_count = 1
    times = get_audio_peaks(audio_clip.get_audio())

    while start_time < video_clip.duration:
        end_time = min(video_clip.duration, start_time + max_segment_length)
        segment_clip = video_clip.subclip(start_time, end_time)

        # 调整速度等操作
        # ...

        # 保存分段视频
        segment_output_path = os.path.join(
            output_folder,
            f"{os.path.splitext(os.path.basename(video_path))[0]}_segment_{segment_count}.mp4"
        )
        segment_clip.write_videofile(segment_output_path, codec='libx264')
        logging.info(f"视频分段处理完成：{segment_output_path}")

        start_time = end_time
        segment_count += 1

    video_clip.close()
    audio_clip.close()      
    import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_audio_clip(audio_path):
    """加载音频剪辑，处理文件不存在的异常。"""
    if not os.path.exists(audio_path):
        logging.error(f"音频文件 {audio_path} 不存在。")
        return None
    return AudioFileClip(audio_path)

def get_audio_peaks(audio_path, sr=22050, threshold=0.05):
    """分析音频文件，找到波峰对应的时间点。"""
    y, sr = librosa.load(audio_path, sr=sr)
    # ... 其他代码 ...

def calculate_speed_based_on_peak(peak_time, video_clip, base_speed=1.0, max_speed_increase=1.0):
    """根据音频波峰调整视频片段的速度。"""
    # ... 其他代码 ...

def adjust_clip_speed_based_on_audio(video_clip, audio_clip):
    """根据音频调整整个视频的速度。"""
    if audio_clip:
        times = get_audio_peaks(audio_clip.filepath)
    else:
        logging.warning("没有音频文件，视频将以正常速度处理。")
        times = [video_clip.duration]
    
    # ... 其他代码 ...

def process_video(video_path, audio_path, output_folder):
    """处理单个视频文件，调整速度并保存结果。"""
    try:
        with VideoFileClip(video_path) as video_clip:
            audio_clip = load_audio_clip(audio_path)
            adjusted_clip = adjust_clip_speed_based_on_audio(video_clip, audio_clip)
            output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0] + '_speed_adjusted.mp4')
            adjusted_clip.write_videofile(output_path)
    except Exception as e:
        logging.error(f"处理视频 {video_path} 时发生错误：{e}")

def main(args):
    """主函数，解析命令行参数，处理视频。"""
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder, exist_ok=True)
    
    for video_file in os.listdir(args.input_video_folder):
        if video_file.endswith('.mp4'):
            video_path = os.path.join(args.input_video_folder, video_file)
            audio_file = os.path.splitext(video_file)[0] + '.mp3'
            audio_path = os.path.join(args.input_audio_folder, audio_file)
            process_video(video_path, audio_path, args.output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    args = parser.parse_args()
    main(args)
    import os
import argparse
from moviepy.editor import VideoFileClip
import librosa
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_clip(path, clip_type):
    """加载音频或视频剪辑，并处理文件不存在的异常。"""
    if clip_type == 'audio' and not os.path.exists(path):
        logging.error(f"文件 {path} 不存在。")
        return None
    return VideoFileClip(path) if clip_type == 'video' else AudioFileClip(path)

def get_audio_peaks(audio_clip, sr=22050, threshold=0.05):
    """分析音频波形，找到波峰对应的时间点。"""
    y, sr = librosa.load(audio_clip.filepath, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    peaks, _ = librosa.find_peaks(D, threshold=threshold)
    times = librosa.frames_to_time(peaks, sr=sr)
    return times

def adjust_clip_speed(video_clip, peak_times):
    """根据音频波峰调整视频片段的速度。"""
    clips = []
    for i, peak_time in enumerate(peak_times):
        if i == 0:
            # 添加视频的开始部分
            clips.append(video_clip.subclip(0, peak_time).set_speed(1.0))
        else:
            # 根据波峰调整速度
            speed = min(1.0 + (peak_time - peak_times[i-1]) / 2, 2.0)  # 示例速度调整逻辑
            clips.append(video_clip.subclip(peak_times[i-1], peak_time).set_speed(speed))
    if peak_times[-1] < video_clip.duration:
        clips.append(video_clip.subclip(peak_times[-1], video_clip.duration).set_speed(1.0))
    return concatenate_videoclips(clips, method="compose")

def process_video(video_path, audio_path, output_folder):
    """处理单个视频文件，根据音频波峰调整速度并保存结果。"""
    video_clip = load_clip(video_path, 'video')
    audio_clip = load_clip(audio_path, 'audio')
    if not video_clip or not audio_clip:
        return

    try:
        peak_times = get_audio_peaks(audio_clip)
        adjusted_clip = adjust_clip_speed(video_clip, peak_times)
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_path))[0] + '_speed_adjusted.mp4')
        adjusted_clip.write_videofile(output_path, codec='libx264')
        logging.info(f"视频处理完成：{output_path}")
    except Exception as e:
        logging.error(f"处理视频时发生错误：{e}")
    finally:
        video_clip.close()
        audio_clip.close()

def main(args):
    """主函数，解析命令行参数，处理视频。"""
    os.makedirs(args.output_folder, exist_ok=True)
    for video_file in os.listdir(args.input_video_folder):
        if video_file.endswith('.mp4'):
            video_path = os.path.join(args.input_video_folder, video_file)
            audio_file = os.path.splitext(video_file)[0] + '.mp3'
            audio_path = os.path.join(args.input_audio_folder, audio_file)
            process_video(video_path, audio_path, args.output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    args = parser.parse_args()
    main(args)


import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_clip(path, clip_type):
    """加载音频或视频剪辑，并处理文件不存在的异常。"""
    if not os.path.exists(path):
        logging.error(f"文件 {path} 不存在。")
        return None
    return VideoFileClip(path) if clip_type == 'video' else AudioFileClip(path)

def get_audio_peaks(audio_clip, sr=22050, threshold=0.05):
    """分析音频波形，找到波峰对应的时间点。"""
    y, sr = librosa.load(audio_clip.filepath, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    peaks, _ = librosa.find_peaks(D, threshold=threshold)
    times = librosa.frames_to_time(peaks, sr=sr)
    return times

def adjust_clip_speed_based_on_peaks(video_clip, peak_times):
    """根据音频波峰调整视频片段的速度，这里简单示例为正常速度，实际逻辑根据需求调整。"""
    clips = [video_clip.subclip(time - 0.1, time + 0.1).set_speed(1.0) for time in peak_times]
    return concatenate_videoclips(clips, method="compose")

def split_clip_into_segments(clip, min_segment_length=60, max_segment_length=300):
    """将视频片段分割成1到5分钟的短视频片段。"""
    segments = []
    start_time = 0
    while start_time < clip.duration:
        end_time = min(start_time + max_segment_length, clip.duration)
        segment = clip.subclip(start_time, end_time)
        segments.append(segment)
        start_time = end_time
        if len(segments) > 0 and segment.duration < min_segment_length:
            # 如果最后一个片段太短，合并回前一个片段
            prev_segment = segments.pop()
            segments[-1] = concatenate_videoclips([prev_segment, segment], method="compose")
    return segments

def process_video_file(video_path, audio_path, output_folder):
    """处理单个视频文件，根据音频波峰合成视频片段，并分割成多个片段保存。"""
    video_clip = load_clip(video_path, 'video')
    audio_clip = load_clip(audio_path, 'audio')
    if not video_clip or not audio_clip:
        return

    try:
        peak_times = get_audio_peaks(audio_clip)
       合成clip = adjust_clip_speed_based_on_peaks(video_clip, peak_times)
        segments = split_clip_into_segments(合成clip)
        for i, segment in enumerate(segments, start=1):
            segment_filename = f"segment_{i:03d}.mp4"
            segment_output_path = os.path.join(output_folder, segment_filename)
            segment.write_videofile(segment_output_path, codec='libx264')
            logging.info(f"视频分段处理完成：{segment_output_path}")
    except Exception as e:
        logging.error(f"处理视频时发生错误：{e}")
    finally:
        video_clip.close()
        audio_clip.close()

def main(args):
    """主函数，解析命令行参数，处理视频。"""
    os.makedirs(args.output_folder, exist_ok=True)
    for video_file in os.listdir(args.input_video_folder):
        if video_file.endswith('.mp4'):
            video_path = os.path.join(args.input_video_folder, video_file)
            audio_file = os.path.splitext(video_file)[0] + '.mp3'
            audio_path = os.path.join(args.input_audio_folder, audio_file)
            process_video_file(video_path, audio_path, args.output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频波峰合成与分段工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    args = parser.parse_args()
    main(args)
    
import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_clip(path, clip_type):
    """加载音频或视频剪辑，并处理文件不存在的异常。"""
    if not os.path.exists(path):
        logging.error(f"文件 {path} 不存在。")
        return None
    return VideoFileClip(path) if clip_type == 'video' else AudioFileClip(path)

def get_audio_peaks(audio_clip, sr=22050, threshold=0.05):
    """分析音频波形，找到波峰对应的时间点。"""
    y, sr = librosa.load(audio_clip.filepath, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    peaks, _ = librosa.find_peaks(D, threshold=threshold)
    times = librosa.frames_to_time(peaks, sr=sr)
    return times

def adjust_clip_speed(video_clip, peak_times, base_speed=1.0, max_speed_increase=1.0):
    """根据音频波峰调整视频片段的速度，并将片段连接起来。"""
    clips = []
    for i in range(len(peak_times)):
        start_time = peak_times[i - 1] if i > 0 else 0
        end_time = peak_times[i] + 0.2  # 加0.2秒作为波峰片段的缓冲
        clips.append(video_clip.subclip(start_time, end_time).set_speed(base_speed))
    return concatenate_videoclips(clips, method="compose")

def split_clip_into_segments(clip, min_segment_length=60, max_segment_length=300):
    """将视频片段分割成1到5分钟的短视频片段。"""
    segments = []
    current_time = 0
    while current_time < clip.duration:
        end_time = min(current_time + max_segment_length, clip.duration)
        segment = clip.subclip(current_time, end_time)
        if segment.duration >= min_segment_length:
            segments.append(segment)
        current_time = end_time
    return segments

def process_clip(video_path, audio_path, output_folder):
    """加载视频和音频剪辑，调整视频速度，并分割视频片段。"""
    video_clip = load_clip(video_path, 'video')
    audio_clip = load_clip(audio_path, 'audio')
    if not video_clip or not audio_clip:
        return

    try:
        peak_times = get_audio_peaks(audio_clip)
        adjusted_clip = adjust_clip_speed(video_clip, peak_times)
        segments = split_clip_into_segments(adjusted_clip)

        for i, segment in enumerate(segments, start=1):
            segment_filename = f"segment_{i:03d}.mp4"
            segment_output_path = os.path.join(output_folder, segment_filename)
            segment.write_videofile(segment_output_path, codec='libx264')
            logging.info(f"视频分段处理完成：{segment_output_path}")

    except Exception as e:
        logging.error(f"处理视频 {video_path} 时发生错误：{e}")
    finally:
        video_clip.close()
        audio_clip.close()
        adjusted_clip.close()

def main(input_video_folder, input_audio_folder, output_folder):
    """主函数，处理视频文件夹中的所有视频文件。"""
    os.makedirs(output_folder, exist_ok=True)
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith('.mp4')]
    audio_files = {os.path.splitext(f)[0] + '.mp3' for f in video_files}

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_clip, video_path, audio_path, output_folder): (video_path, audio_path)
                   for video_path, audio_path in
                   ((os.path.join(input_video_folder, video_file), os.path.join(input_audio_folder, audio_file))
                    for video_file in video_files
                    if audio_file in audio_files)}

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"处理视频时发生错误：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频波峰合成与分段工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    args = parser.parse_args()
    main(**vars(args))
    
from concurrent.futures import ThreadPoolExecutor
import os

# 示例：使用多线程来并行处理视频文件
def process_video_concurrently(video_files, audio_files, output_folder):
    with ThreadPoolExecutor(max_workers=len(video_files)) as executor:
        futures = {executor.submit(process_video, video, audio, output_folder): (video, audio)
                   for video, audio in zip(video_files, audio_files)}
        for future in futures:
            future.result()  # 等待任务完成

# 示例：使用局部变量代替全局变量
def get_audio_peaks(audio_data, sr=22050, threshold=0.05):
    local_y, local_sr = librosa.load(audio_data, sr=sr)  # 使用局部变量
    # ...处理逻辑...

# 示例：预计算和缓存结果
def calculate_and_cache_results(repetitive_computation_func, *args):
    cache = {}
    def wrapped(*args):
        if args not in cache:
            cache[args] = repetitive_computation_func(*args)
        return cache[args]
    return wrapped

# 示例：使用生成器处理大数据集
def process_large_dataset(data):
    for item in data:
        yield process_item(item)  # 假设 process_item 是一个处理函数

# 示例：优化数据结构，使用集合进行成员检查
def check_membership(item, collection):
    if isinstance(collection, set):
        return item in collection  # 集合的成员检查更快
    else:
        return item in list(collection)
        
        import os
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import librosa
import numpy as np
import logging
from concurrent.futures import ThreadPoolExecutor

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_clip(path, clip_type):
    """加载音频或视频剪辑，并处理文件不存在的异常。"""
    if not os.path.exists(path):
        logging.error(f"文件 {path} 不存在。")
        return None
    return VideoFileClip(path) if clip_type == 'video' else AudioFileClip(path)

def get_audio_peaks(audio_path, sr=22050, threshold=0.05):
    """分析音频文件，找到波峰对应的时间点。"""
    y, sr = librosa.load(audio_path, sr=sr)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    peaks, _ = librosa.find_peaks(D, threshold=threshold)
    times = librosa.frames_to_time(peaks, sr=sr)
    return times

def adjust_clip_speed_based_on_peaks(video_clip, peak_times, base_speed=1.0, max_speed_increase=1.0):
    """根据音频波峰调整视频片段的速度，并将片段连接起来。"""
    clips = []
    for i in range(len(peak_times)):
        start_time = peak_times[i - 1] if i > 0 else 0
        end_time = peak_times[i] + 0.2  # 加0.2秒作为波峰片段的缓冲
        speed_increase = min(max_speed_increase, (end_time - start_time) / 0.2)
        new_speed = base_speed + speed_increase
        clips.append(video_clip.subclip(start_time, end_time).set_speed(new_speed))
    return concatenate_videoclips(clips, method="compose")

def process_clip(args):
    video_path, audio_path, output_folder, sr, threshold = args
    try:
        video_clip = load_clip(video_path, 'video')
        audio_clip = load_clip(audio_path, 'audio')
        if not video_clip or not audio_clip:
            logging.error("无法加载视频或音频文件。")
            return

        peak_times = get_audio_peaks(audio_clip.filepath, sr, threshold)
        adjusted_clip = adjust_clip_speed_based_on_peaks(video_clip, peak_times)

        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_folder, f"{base_name}_speed_adjusted.mp4")
        adjusted_clip.write_videofile(output_path, codec='libx264')
        logging.info(f"视频处理完成：{output_path}")
    except Exception as e:
        logging.error(f"处理视频 {video_path} 时发生错误：{e}")
    finally:
        if video_clip and video_clip.is_opened:
            video_clip.close()
        if audio_clip and audio_clip.is_opened:
            audio_clip.close()
        if adjusted_clip and adjusted_clip.is_opened:
            adjusted_clip.close()

def main(input_video_folder, input_audio_folder, output_folder, sr=22050, threshold=0.05, max_workers=4):
    os.makedirs(output_folder, exist_ok=True)
    video_files = [f for f in os.listdir(input_video_folder) if f.endswith('.mp4')]
    video_paths = [os.path.join(input_video_folder, f) for f in video_files]

    arguments = [
        (video_path, os.path.join(input_audio_folder, os.path.splitext(os.path.basename(video_path))[0] + '.mp3'),
         output_folder, sr, threshold) for video_path in video_paths
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for args in arguments:
            executor.submit(process_clip, args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频速度调整工具")
    parser.add_argument("--input_video_folder", required=True, help="输入视频文件夹路径")
    parser.add_argument("--input_audio_folder", required=True, help="输入音频文件夹路径")
    parser.add_argument("--output_folder", required=True, help="输出文件夹路径")
    parser.add_argument("--sr", type=int, default=22050, help="音频采样率")
    parser.add_argument("--threshold", type=float, default=0.05, help="音频峰值检测阈值")
    parser.add_argument("--max_workers", type=int, default=4, help="最大线程数")

    args = parser.parse_args()
    main(**vars(args))