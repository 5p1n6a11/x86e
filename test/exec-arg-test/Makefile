TARGET = test.bin
OBJS = crt0.o test.o
Z_TOOLS = ../z_tools

CC = gcc
LD = ld
AS = nasm
CFLAGS += -nostdlib -fno-asynchronous-unwind-tables \
	-I$(Z_TOOLS)/i386-elf-gcc/include -g -fno-stack-protector \
	-m32 -fno-pie -O0 -march=i386 -fcf-protection=none -mmanual-endbr # endbr32
LDFLAGS += --entry=start --oformat=binary -Ttext 0x7c00 -m elf_i386

.PHONY: all clean
all :
	make $(TARGET)

%.o : %.c Makefile
	$(CC) $(CFLAGS) -c $<

%.o : %.asm Makefile
	$(AS) -f elf $<

$(TARGET) : $(OBJS) Makefile
	$(LD) $(LDFLAGS) -o $@ $(OBJS)

clean :
	rm *.o
	rm *.bin

