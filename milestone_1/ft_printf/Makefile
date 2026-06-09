NAME = libftprintf.a

CC = cc

CFLAGS = -Wall -Wextra -Werror

RM = rm -rf

SRC =ft_printf.c\
	ft_putchar.c\
	ft_puthex.c\
	ft_putnbr.c\
	ft_putstr.c\
	ft_putunsig.c\
	ft_putvoid.c

OBJS = $(SRC:.c=.o)

%.o : %.c
	$(CC) $(CFLAGS) -c -o $@ $<

all: $(NAME)

$(NAME) : $(OBJS)
	@ar crs $(NAME) $(OBJS)

clean:
	@$(RM) $(OBJS)

fclean: clean
	@$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re