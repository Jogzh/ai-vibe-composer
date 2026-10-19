# 贡献 / Contributing

欢迎贡献可复用音色、合成配方、音频工具、文档和修复。Welcome reusable sounds, synthesis recipes, audio tools, documentation and fixes.

1. 从模板创建仓库或 fork，安装 Node.js >=22.12 并运行 `npm ci`。
2. 代码提交标题与说明使用中文，技术名称可保留英文。Use Chinese commit titles/bodies; technical names may remain English.
3. 新音频放在合适的 `public/audio/` 子目录，附作者、原始 URL、明确可再分发的许可与处理记录。Do not assume an online file can be redistributed.
4. 提供根 MIDI、BPM/小节（适用时），更新本库 manifest，再执行 `npm run assets:catalog`。保留原录音的散列与许可。
5. 不提交歌曲成品、歌曲专属谱面/脚本、个人录音、人声分轨、模型、缓存、API Key。可复用短循环须明确标注为素材并给出许可。
6. 音乐相关修复交付可播放的本地对比文件；区分参考资料、客观测量与真正耳听。不把测试通过写成好听。

验证 / Validation:

```sh
npm test
npm run build
npm run test:browser
npm run test:palette
npm run assets:check
python -m unittest discover -s tests -p 'test_*.py'
python scripts/build_sound_palette.py verify
```

浏览器检查需要 Playwright Chromium，Python 测试需要轻量依赖，音频 DSP 需要 FFmpeg。可选 Demucs 不属于默认 CI。PR 中说明修改目的、真实验证结果、人工试听状态及素材许可变化。
