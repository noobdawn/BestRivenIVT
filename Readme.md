# BestRivenIVT: 《驱入虚空》自动化配卡工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](Readme_en.md) | [中文](Readme.md)

## 概述
本项目旨在为《驱入虚空》游戏开发一个自动化配卡工具，通过算法在特定环境和敌人情况下，寻找使武器DPS最大化的MOD组合最优解。通过遍历所有可能的MOD组合并计算伤害输出，为玩家提供数据驱动的配卡方案。

## 依赖库
- numpy
- unittest

## TODO 列表
- [✅] 直接伤害计算公式
- [✅] DoT伤害计算公式
- [✅] 元素触发与增伤影响
- [✅] 遍历组合并寻求最优解
- [❌] 使用OCR读取游戏
- [❌] 实现GUI界面
- [❌] 完善步枪外的配卡数据
- [❌] 完善所有枪械数据
- [❌] 增加1.2版本空中系列卡牌伤害计算公式