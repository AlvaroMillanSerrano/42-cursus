NAME = push_swap

CC = cc

CFLAGS = -Wall -Wextra -Werror

RM = rm -rf

SRC =ft_push_swap.c\
	ft_push_swap_utils.c\
	ft_stack_utils.c\
	ft_check_errors.c\
	ft_split.c\
	ft_push.c\
	ft_swap.c\
	ft_rotate.c\
	ft_reverse_rotate.c\
	ft_sort.c\
	ft_sort_utils.c

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