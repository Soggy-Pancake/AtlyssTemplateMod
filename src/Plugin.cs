using System;
using System.Linq;
using System.Collections.Generic;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using CodeTalker.Packets;
using CodeTalker.Networking;
using Mirror;

namespace AtlyssTemplateMod;
#pragma warning disable CS8618

[BepInPlugin(PluginInfo.GUID, PluginInfo.NAME, PluginInfo.VERSION)]
public class Plugin : BaseUnityPlugin {

    public static Plugin _plugin;
    internal static Harmony _harmony;
    internal static ManualLogSource logger;

    private void Awake() {
        _plugin = this;
        logger = Logger;
        _harmony = new Harmony(PluginInfo.GUID);

        logger.LogInfo("TemplateMod loaded!");

        //_harmony.PatchAll(typeof(Patches));
        //logger.LogInfo("Patch successful! Registering network listeners...");
    }

    private void Update() { }

    private void FixedUpdate() { }
}