MAJOR_VERSION = 0
MEDIUM_VERSION = 0
MINOR_VERSION = 1

SYSTEM_DIR := ../../../..
CCP_DIR := ${SYSTEM_DIR}/utility/tools/ccp_adapt
WAPI_DIR := ../example

CC := gcc

include ./conf/src_files.mk

INC_FLAGS += -I./include
INC_FLAGS += -I./include/wapis
#INC_FLAGS += -I./include/ccp_adapt
INC_FLAGS += -I$(CCP_DIR)/adapt/include

JSON_GEN = src/wapis_json_generator.py
CONFIG_CONV = src/json_converter.py
SRC_GEN = src/src_generator.py

SHARED_LIB_LINK += -llibs -llibwapis
SHARED_LIB_LINK += -llibs -llibwmccpadapt
LIB_NAME := libwapis_example.dll

TARGET_BOARD := WLXP0400_AND_EVB

#CCP_ADAPT_MAIN_BUILD := 1

# Compiler Flags

ifeq ($(CCP_ADAPT_MAIN_BUILD), )
CFLAGS := -D__WM_SHARE_LIBRARY__      # Enable Share library building
LIB_CFLAGS := -fPIC -shared
TARGET_OUT := $(LIB_NAME)
else
TARGET_OUT := wm_apis
endif

CFLAGS += -Wall
CFLAGS += -O2                         # Optimization=
CFLAGS += -std=gnu99                  # Enable GNU99
CFLAGS += $(INC_FLAGS)
CFLAGS += -D$(TARGET_BOARD)
CFLAGS := $(strip $(CFLAGS))

CFLAGS += -Wno-incompatible-pointer-types
#CFLAGS += -Wall -Werror -Wextra      # Warnings

TEST_FILES := src/wapis_example_main.c

.PHONY: all
all:
	rm -rf bin
	python $(JSON_GEN);
	python $(CONFIG_CONV) --exclude-others;
	python $(SRC_GEN);
	
	$(CC) $(LIB_CFLAGS) $(CFLAGS) $(SHARED_LIB_LINK) $(SRC_FILES) -o libs/$(TARGET_OUT)

.PHONY: clean
clean:
	rm -rf libs/$(LIB_NAME)*
	rm -rf bin
	rm conf/wapi_config.json

.PHONY: install
install:
	mkdir bin
	cp conf/ccp_adapt.json bin/ -rf
	cp $(CCP_DIR)/adapt/include bin/ -rf
	cp libs/*.dll bin/ -rf

.PHONY: test
test:
	$(CC) $(CFLAGS) -Ibin/include -Ibin \
		$(SHARED_LIB_LINK) -llibwapis_example $(TEST_FILES) -o bin/wapis_example

.PHONY: update
update:
	python $(JSON_GEN);
	python $(CONFIG_CONV) --exclude-others;
	python $(SRC_GEN);

.PHONY: instest
instest:
	mkdir bin
	cp conf/ccp_adapt.json bin/ -rf
	cp $(CCP_DIR)/adapt/include bin/ -rf
	cp libs/*.dll bin/ -rf
	
	$(CC) $(CFLAGS) -Ibin/include -Ibin \
		$(SHARED_LIB_LINK) -llibwapis_example $(TEST_FILES) -o bin/wapis_example