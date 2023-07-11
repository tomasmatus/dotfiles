import vapoursynth as vs
from lvsfunc.denoise import detail_mask
from vsutil import depth
from kagefunc import adaptive_grain
core = vs.core

core.max_cache_size = 2248
core.num_threads = 4


clip = video_in

dither = core.resize.Bicubic(clip, format=vs.YUV420P16, dither_type='error_diffusion')

mask = detail_mask(dither, pre_denoise=None, rad=3, radc=2, brz_a=2500, brz_b=1500)

deband = core.neo_f3kdb.Deband(dither, 17, 48, 36, 36, 12, 4, keep_tv_range=True, output_depth=16)
db = core.std.MaskedMerge(deband, dither, mask)

grain = adaptive_grain(db, strength=1, luma_scaling=6, static=False)
out = core.resize.Bicubic(grain, format=vs.YUV420P8, dither_type='error_diffusion')

out.set_output()