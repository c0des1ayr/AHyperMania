#ifndef OBJ_SPECIALRING_H
#define OBJ_SPECIALRING_H

#include "GameAPI/Game.h"

// =============================================================================

// Definitions -----------------------------------------------------------------

// =============================================================================
typedef struct {
	RSDK_OBJECT
	uint16 aniFrames;
	Hitbox hitbox;
	uint16 sfxSpecialRing;
	uint16 sfxSpecialWarp;
	uint16 modelIndex;
	uint16 sceneIndex;
} ObjectSpecialRing;

typedef struct {
	RSDK_ENTITY
	StateMachine(state);
	int32 id;
	int32 planeFilter;
	int32 warpTimer;
	int32 sparkleRadius;
	Animator warpAnimator;
	int32 angleZ;
	int32 angleY;
	bool32 enabled;
	Matrix matTempRot;
	Matrix matTransform;
	Matrix matWorld;
	Matrix matNormal;
} EntitySpecialRing;

extern ObjectSpecialRing* SpecialRing;

// =============================================================================

// Functions -------------------------------------------------------------------

// =============================================================================
extern void (*SpecialRing_State_Flash)();
extern void (*SpecialRing_State_Warp)();

void SpecialRing_State_HPZ_Warp();

bool32 SpecialRing_State_Idle_HOOK(bool32);
bool32 SpecialRing_State_Flash_HOOK(bool32);

void SpecialRing_Draw_OVERLOAD();

#define OBJ_SPECIALRING_SETUP \
  IMPORT_PUBLIC_FUNC(SpecialRing_State_Flash); \
  IMPORT_PUBLIC_FUNC(SpecialRing_State_Warp); \
  HOOK_STATE(SpecialRing_State_Idle, 1); \
  HOOK_IMPORTED_STATE(SpecialRing_State_Flash, 1); \
  MOD_REGISTER_OBJ_OVERLOAD(SpecialRing, NULL, NULL, NULL, SpecialRing_Draw_OVERLOAD, NULL, NULL, NULL, NULL, NULL)

#endif //! OBJ_SPECIALRING_H
