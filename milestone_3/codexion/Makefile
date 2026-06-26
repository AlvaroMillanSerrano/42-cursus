NAME = codexion

CC = cc

CFLAGS = -Wall -Wextra -Werror

RM = rm -rf

SRC =coders/main.c\
	coders/validation.c\
	coders/heap.c\
	coders/actions.c\
	coders/codexion.c\
	coders/simulation.c\
	coders/monitor.c\
	coders/simulation_utils.c

OBJS = $(SRC:.c=.o)

%.o : %.c
	$(CC) $(CFLAGS) -c -o $@ $<

all: $(NAME)

$(NAME) : $(OBJS)
	$(CC) $(CFLAGS) -o $(NAME) $(OBJS)

clean:
	@$(RM) $(OBJS)

fclean: clean
	@$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
