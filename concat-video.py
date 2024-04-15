from moviepy.editor import VideoFileClip, concatenate_videoclips


clip_1 = VideoFileClip("hologram.mp4")
clip_2 = VideoFileClip("hologram1.mp4")
clip_3 = VideoFileClip("hologram2.mp4")
clip_4 = VideoFileClip("hologram3.mp4")
final_clip = concatenate_videoclips([clip_1,clip_2,clip_3,clip_4])
final_clip.write_videofile("final.mp4")
