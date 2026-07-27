MAJOR_VERSION = 0
MEDIUM_VERSION = 0
MINOR_VERSION = 1

# Add environment variable to avoid error in release doc
ifeq ($(RELEASE_ENVIR),1)
    SYSTEM_DIR := $(CURDIR)/..
else
    SYSTEM_DIR := $(CURDIR)/../..
endif

CC := gcc

INC_FLAGS += -I$(SYSTEM_DIR)/include

LIB_NAME := libwapi.so

# In release environment, use the library in project
ifeq ($(RELEASE_ENVIR),1)
    SHARED_LIB_LINK += -L$(SYSTEM_DIR)/../../../system/ci/host/libs -llibUSB2UARTSPIIIC
    SHARED_LIB_LINK += -L$(SYSTEM_DIR)/../../../system/ci/host/libs -lwmccpframe
else
    SHARED_LIB_LINK += -L$(SYSTEM_DIR)/ci/host/libs -llibUSB2UARTSPIIIC
    SHARED_LIB_LINK += -L$(SYSTEM_DIR)/ci/host/libs -lwmccpframe
endif

CFLAGS += -O2                    # Optimization
CFLAGS += -Wall -Werror -Wextra  # Warnings
CFLAGS += -std=gnu99             # Enable GNU99
CFLAGS += $(INC_FLAGS)
#CFLAGS += -DCONFIG_WM_WAPI_RESERVED
CFLAGS := $(strip $(CFLAGS))

SRC_FILES := $(wildcard ../ccp/*.c ../lib/*.c ../wapis/*.c *.c)

# Find lib source files
ifeq ($(RELEASE_ENVIR),1)
    LIB_SRC_FILES := $(wildcard ../wapis/*.c)
else
    LIB_SRC_FILES := $(wildcard $(SYSTEM_DIR)/wapis/*.c)
    LIB_SRC_FILES := $(filter-out $(SYSTEM_DIR)/wapis/wm_serial_api.c,$(LIB_SRC_FILES))
    LIB_SRC_FILES := $(filter-out $(SYSTEM_DIR)/wapis/wm_serial_api_command_sanity_checker.c,$(LIB_SRC_FILES))
endif

TARGET_FILE := wapi_example

.PHONY: all
all: clean
	$(CC) $(CFLAGS) $(SRC_FILES) -o $(TARGET_FILE)

.PHONY: clean
clean:
	rm -rf $(TARGET_FILE)

lib:
	rm -rf $(LIB_NAME)*
	@echo "gcc command is executed and the command line is hidden"
	@$(CC) -fpic -shared $(CFLAGS) $(LIB_SRC_FILES) $(SHARED_LIB_LINK) -o $(LIB_NAME).$(MAJOR_VERSION).$(MEDIUM_VERSION).$(MINOR_VERSION)
	ln -s $(LIB_NAME).$(MAJOR_VERSION).$(MEDIUM_VERSION).$(MINOR_VERSION) $(LIB_NAME)

lib_install: lib
	cp -rf $(LIB_NAME)* $(SYSTEM_DIR)/ci/host/libs