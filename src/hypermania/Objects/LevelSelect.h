#ifndef OBJ_LEVELSELECT_H
#define OBJ_LEVELSELECT_H

#include "GameAPI/Game.h"

typedef enum {
	LSELECT_PLAYER_NONE,
	LSELECT_PLAYER_SONIC,
	LSELECT_PLAYER_TAILS,
	LSELECT_PLAYER_KNUCKLES,
#if MANIA_USE_PLUS
	LSELECT_PLAYER_MIGHTY,
	LSELECT_PLAYER_RAY,
#endif
} LevelSelectPlayerIDs;

typedef struct {
	RSDK_OBJECT
#if MANIA_USE_PLUS
	STATIC(int32 bgAniDuration, 240);
	TABLE(int32 bgAniDurationTable[4], { 240, 3, 3, 3 });
	TABLE(int32 cheat_RickyMode[9], { 1, 9, 7, 9, 0, 8, 1, 1, 255 });
	TABLE(int32 cheat_AllEmeralds[5], { 4, 1, 2, 6, 255 });
	TABLE(int32 cheat_MaxContinues[9], { 1, 9, 9, 2, 1, 1, 2, 4, 255 });
	TABLE(int32 cheat_SwapGameMode[9], { 2, 0, 1, 8, 0, 6, 2, 3, 255 });
	TABLE(int32 cheat_UnlockAllMedals[9], { 1, 9, 8, 9, 0, 5, 0, 1, 255 });
	TABLE(int32 cheat_SuperDash[9], { 2, 0, 1, 7, 0, 8, 1, 5, 255 });
	TABLE(int32 cheat_MaxControl[5], { 9, 0, 0, 1, 255 });
	TABLE(int32 cheat_ToggleSuperMusic[9], { 6, 2, 1, 4, 255, 0, 0, 0, 0 });
	int32 bgAniFrame;
	int32 startMusicID;
	int32 soundTestMax;
	uint16 sfxFail;
	uint16 sfxRing;
	uint16 sfxEmerald;
	uint16 sfxContinue;
	uint16 sfxMedalGot;
	int32* cheatCodePtrs[8];
	int32 cheatCodePos[8];
	void (*checkCheatActivated[8])();
#else
	STATIC(int32 bgAniDuration, 240);
	int32 bgAniFrame;
	TABLE(int32 bgAniDurationTable[4], { 240, 3, 3, 3 });
	int32 startMusicID;
	int32 soundTestMax;
	uint16 sfxFail;
#endif
} ObjectLevelSelect;

typedef struct {
	RSDK_ENTITY
	StateMachine(state);
	StateMachine(stateDraw);
	int32 timer;
	int32 labelID;
	int32 soundTestID;
	int32 leaderCharacterID;
	int32 sidekickCharacterID;
	// don't feel like copy pasting these types so i made them all void* :>)
	void* zoneNameLabels[32];
	void* stageIDLabels[32];
	void* soundTestLabel;
	void* zoneIcon;
	void* player1Icon;
	void* player2Icon;
#if MANIA_USE_PLUS
	void* pinballLabel;
#endif
	int32 labelCount;
#if MANIA_USE_PLUS
	int32 offsetUFO;
	int32 offsetBSS;
	int32 unused1;
	int32 unused2;
	int32 unused3;
	int32 unused4;
#endif
} EntityLevelSelect;

extern ObjectLevelSelect* LevelSelect;

// =============================================================================

// Functions -------------------------------------------------------------------

// =============================================================================
void LevelSelect_StageLoad_OVERLOAD();

#define OBJ_LEVELSELECT_SETUP \
  MOD_REGISTER_OBJ_OVERLOAD(LevelSelect, NULL, NULL, NULL, NULL, NULL, LevelSelect_StageLoad_OVERLOAD, NULL, NULL, NULL)

void LevelSelect_Cheat_AllEmeralds();

#endif //! OBJ_LEVELSELECT_H
