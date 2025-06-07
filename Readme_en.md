# BestRivenIVT: Automated Modding Tool for 'Into the Void'

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](Readme_en.md) | [中文](Readme.md)

## Overview
This project is designed for the game 'Into the Void' to provide an automated modding tool. It seeks the optimal MOD combination that maximizes weapon DPS under specific environments and enemies by algorithmically evaluating all possible configurations.

## Dependencies
- numpy
- unittest

## Usage

Refer to `seek.py` for implementation details.

Assume we have a Riven Mod with the following attributes:

![](/assets/目标紫卡.jpg)

The user of waterdrop is Nian Chunqiu, whose mod configuration is as follows:

![](/assets/角色MOD.jpg)

After adjusting environment settings based on the mod configuration and equipping the target Riven Mod on the weapon, execute the script.

The optimal DPS and best MOD combination calculated by the script are shown below:

![](assets/伤害Log.jpg)

Below are the actual effects observed in the training ground (character remained stationary during shooting; sliding motion was caused by screenshot hotkey). The calculated non-critical hits correspond to Tier 1 criticals, while critical hits correspond to Tier 2 criticals, demonstrating close alignment with the result.

![](/assets/伤害实测.jpg)

## TODO List
- [✅] Direct damage calculation formula
- [✅] DoT damage calculation formula
- [✅] Elemental trigger and damage bonus effects
- [✅] Traverse combinations and seek optimal solution
- [❌] Use OCR to read game data
- [❌] Implement GUI interface
- [❌] Complete modding data for non-rifle weapons
- [❌] Complete data for all firearm types
- [❌] Add damage formula for aerial series cards (v1.2)