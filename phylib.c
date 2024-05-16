#include "phylib.h"

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){

    phylib_object *still_ball_object = malloc(sizeof(phylib_object));

    (*still_ball_object).type = PHYLIB_STILL_BALL;

    (*still_ball_object).obj.still_ball.number = number;

    (*still_ball_object).obj.still_ball.pos.x = pos->x;
    (*still_ball_object).obj.still_ball.pos.y = pos->y;

    return still_ball_object;
}


phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){

    phylib_object *rolling_ball_object = malloc(sizeof(phylib_object));

    if (rolling_ball_object == NULL){
        return NULL;
    }

    (*rolling_ball_object).type = PHYLIB_ROLLING_BALL;

    (*rolling_ball_object).obj.rolling_ball.number = number;

    (*rolling_ball_object).obj.rolling_ball.pos.x = pos->x;
    (*rolling_ball_object).obj.rolling_ball.pos.y = pos->y;

    (*rolling_ball_object).obj.rolling_ball.vel.x = vel->x;
    (*rolling_ball_object).obj.rolling_ball.vel.y = vel->y;

    (*rolling_ball_object).obj.rolling_ball.acc.x = acc->x;
    (*rolling_ball_object).obj.rolling_ball.acc.y = acc->y;

    return rolling_ball_object;
}

phylib_object *phylib_new_hole( phylib_coord *pos ){

    phylib_object *hole_object = malloc(sizeof(phylib_object));

    if (hole_object == NULL){
        return NULL;
    }

    (*hole_object).type = PHYLIB_HOLE;

    (*hole_object).obj.hole.pos.x = pos->x;
    (*hole_object).obj.hole.pos.y = pos->y;

    return hole_object;
}

phylib_object *phylib_new_hcushion( double y ){

    phylib_object *hcushion_object = malloc(sizeof(phylib_object));

    if (hcushion_object == NULL){
        return NULL;
    }

    (*hcushion_object).type = PHYLIB_HCUSHION;

    (*hcushion_object).obj.hcushion.y = y;

    return hcushion_object;
}

phylib_object *phylib_new_vcushion( double x ){

    phylib_object *vcushion_object = malloc(sizeof(phylib_object));

    if (vcushion_object == NULL){
        return NULL;
    }

    (*vcushion_object).type = PHYLIB_VCUSHION;

    (*vcushion_object).obj.vcushion.x = x;

    return vcushion_object;
}

phylib_table *phylib_new_table( void ){

    phylib_table *table = malloc(sizeof(phylib_table));

    if (table == NULL){
        return NULL;
    }

    table->time = 0.0;

    table->object[0] = phylib_new_hcushion(0.0); // y = 0
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); // y = L
    table->object[2] = phylib_new_vcushion(0.0); // x = 0
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); // x = W

    // top right hole
    phylib_coord position;
    position.x = 0.0;
    position.y = 0.0;

    // top left hole
    phylib_coord position4;
    position4.x = PHYLIB_TABLE_WIDTH;
    position4.y = 0.0;

    // bottom left hole
    phylib_coord position3;
    position3.x = 0.0;
    position3.y = PHYLIB_TABLE_LENGTH;

    // bottom right hole
    phylib_coord position6;
    position6.x = PHYLIB_TABLE_WIDTH;
    position6.y = PHYLIB_TABLE_LENGTH;

    // left middle hole
    phylib_coord position2;
    position2.x = 0.0;
    position2.y = PHYLIB_TABLE_LENGTH / 2;

    // right middle hole
    phylib_coord position5;
    position5.x = PHYLIB_TABLE_WIDTH;
    position5.y = PHYLIB_TABLE_LENGTH / 2;

    table->object[4] = phylib_new_hole(&position);
    table->object[5] = phylib_new_hole(&position2);
    table->object[6] = phylib_new_hole(&position3);
    table->object[7] = phylib_new_hole(&position4);
    table->object[8] = phylib_new_hole(&position5);
    table->object[9] = phylib_new_hole(&position6);

    for (int a = 10; a < PHYLIB_MAX_OBJECTS; a++){
        table->object[a] = NULL;
    }

    return table;
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    if (*src != NULL){
        phylib_object *copiedObject = malloc(sizeof(phylib_object));

        if (copiedObject == NULL){
            return;
        }
        *dest = copiedObject;

        memcpy(*dest, *src, sizeof(phylib_object));
    }
}

phylib_table *phylib_copy_table( phylib_table *table ){

    phylib_table * copiedTable = malloc(sizeof(phylib_table));

    if (copiedTable == NULL){
        return NULL;
    }

    (*copiedTable).time = (*table).time;
    for (int e = 0; e < PHYLIB_MAX_OBJECTS; e++){
        phylib_copy_object(&copiedTable->object[e], &table->object[e]);
    }

    return copiedTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ){

    int c = 0;

    while (table->object[c] != NULL && c < PHYLIB_MAX_OBJECTS){
        c++;
    }

    table->object[c] = object;
}

void phylib_free_table( phylib_table *table ){

    for (int d = 0; d < PHYLIB_MAX_OBJECTS; d++){
        if (table->object[d] != NULL){
            free(table->object[d]);
            table->object[d] = NULL;
        }
    }

    free(table);
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

    phylib_coord subbed;
    subbed.x = c1.x - c2.x;
    subbed.y = c1.y - c2.y;

    return subbed;
}

double phylib_length( phylib_coord c ){

    double length = sqrt((c.x * c.x) + (c.y * c.y));

    return length;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){

    double dot = (a.x * b.x) + (a.y * b.y);

    return dot;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    if ((*obj1).type != 1){ // obj1 must be a PHYLIB_ROLLING_BALL; 
        return -1.0;
    }

    double distance = 0;

    if ((*obj2).type == 0){ // If obj2 is stillBALL
        distance = (phylib_length(phylib_sub((*obj1).obj.rolling_ball.pos, (*obj2).obj.still_ball.pos))) - PHYLIB_BALL_DIAMETER;
    }
    else if ((*obj2).type == 1){ // If obj2 is a rollingBall
        distance = (phylib_length(phylib_sub((*obj1).obj.rolling_ball.pos, (*obj2).obj.rolling_ball.pos))) - PHYLIB_BALL_DIAMETER;
    }
    else if ((*obj2).type == 2){ // If obj2 is a hole
        distance = phylib_length(phylib_sub((*obj1).obj.rolling_ball.pos, (*obj2).obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
    }
    else if ((*obj2).type == 3){ // If obj2 is a Hcushion
        distance = (fabs((*obj1).obj.rolling_ball.pos.y - (*obj2).obj.hcushion.y) - PHYLIB_BALL_RADIUS);
    }
    else if ((*obj2).type == 4){ // If obj2 is a Vcushion
        distance = (fabs((*obj1).obj.rolling_ball.pos.x - (*obj2).obj.vcushion.x) - PHYLIB_BALL_RADIUS);
    }
    else{
        return -1.0;
    }

    return distance;
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ){

    if ((*new).type == 1 && (*old).type == 1){

        (*new).obj.rolling_ball.pos.x = (*old).obj.rolling_ball.pos.x + ((*old).obj.rolling_ball.vel.x * time) +
        (0.5 * (*old).obj.rolling_ball.acc.x * (time * time));
        (*new).obj.rolling_ball.pos.y = (*old).obj.rolling_ball.pos.y + ((*old).obj.rolling_ball.vel.y * time) +
        (0.5 * (*old).obj.rolling_ball.acc.y * (time * time));

        (*new).obj.rolling_ball.vel.x = (*old).obj.rolling_ball.vel.x + ((*old).obj.rolling_ball.acc.x * time);
        (*new).obj.rolling_ball.vel.y = (*old).obj.rolling_ball.vel.y + ((*old).obj.rolling_ball.acc.y * time);
        roll_constraint(new, old);
    }
}

void roll_constraint( phylib_object *new, phylib_object *old){

    if (((*old).obj.rolling_ball.vel.x > 0 && (*new).obj.rolling_ball.vel.x < 0) ||
    ((*old).obj.rolling_ball.vel.x < 0 && (*new).obj.rolling_ball.vel.x > 0)){ // Velocity x changed sign
        (*new).obj.rolling_ball.vel.x = 0;
        (*new).obj.rolling_ball.acc.x = 0;
    }
    
    if (((*old).obj.rolling_ball.vel.y > 0 && (*new).obj.rolling_ball.vel.y < 0) ||
    ((*old).obj.rolling_ball.vel.y < 0 && (*new).obj.rolling_ball.vel.y > 0)){ // Velocity y changed sign
        (*new).obj.rolling_ball.vel.y = 0;
        (*new).obj.rolling_ball.acc.y = 0;
    }
}

unsigned char phylib_stopped( phylib_object *object ){

    double speed = phylib_length((*object).obj.rolling_ball.vel);

    if (speed < PHYLIB_VEL_EPSILON){
        (*object).type = PHYLIB_STILL_BALL;
        (*object).obj.still_ball.number =(*object).obj.rolling_ball.number;
        (*object).obj.still_ball.pos.x =(*object).obj.rolling_ball.pos.x;
        (*object).obj.still_ball.pos.y =(*object).obj.rolling_ball.pos.y;
        return 1;
    }
    else {
        return 0;
    }

}

void phylib_bounce( phylib_object **a, phylib_object **b ){


    switch((*b)->type){
        case 3: // Hcushion - angle of incidence == angle of reflection
            (*a)->obj.rolling_ball.vel.y = ((*a)->obj.rolling_ball.vel.y) * (-1);
            (*a)->obj.rolling_ball.acc.y = ((*a)->obj.rolling_ball.acc.y) * (-1);
            break;
        case 4: // Vcushion
            (*a)->obj.rolling_ball.vel.x = ((*a)->obj.rolling_ball.vel.x) * (-1);
            (*a)->obj.rolling_ball.acc.x = ((*a)->obj.rolling_ball.acc.x) * (-1);
            break;
        case 2: // Hole - delete the ball from the table
            free(*a);
            *a = NULL;
            break;
        case 0: // StillBall - turns into rollingBall then applies rollingBall bounce physics
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
            (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;
            (*b)->obj.rolling_ball.vel.x = 0;
            (*b)->obj.rolling_ball.vel.y = 0;
            (*b)->obj.rolling_ball.acc.x = 0;
            (*b)->obj.rolling_ball.acc.y = 0;
        case 1: // Rolling Ball - rollingBall bounce physics
            rollingBallBounce(a,b);
            break;
    }
}

void rollingBallBounce( phylib_object **a, phylib_object **b ){

    // For phylib_sub(a, b) - you get a - b
    // Compute the position of a with respect to b
    phylib_coord r_ab;
    r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

    // Compute the relative velocity of a with respect to b
    phylib_coord v_rel;
    v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

    // Divide the x and y components of r_ab by the length of r_ab to get normal vector n
    phylib_coord n;
    double length = phylib_length(r_ab);
    n.x = r_ab.x / length;
    n.y = r_ab.y / length;

    // Calculate the ratio of the relative velocity, v_rel, in the direction of ball a
    double v_rel_n;
    v_rel_n = phylib_dot_product(n, v_rel);

    // Update the x velocity of ball a by subtracting v_rel_n multipied by the x component of
    // vector n. Similarly, Update the x velocity of ball a by subtracting v_rel_n multipied by
    // the x component of vector n.
    (*a)->obj.rolling_ball.vel.x = ((*a)->obj.rolling_ball.vel.x) - (v_rel_n * n.x);
    (*a)->obj.rolling_ball.vel.y = ((*a)->obj.rolling_ball.vel.y) - (v_rel_n * n.y);

    // Update the x and y velocities of ball b by adding the product of v_rel_n and vector n
    (*b)->obj.rolling_ball.vel.x = ((*b)->obj.rolling_ball.vel.x) + (v_rel_n * n.x);
    (*b)->obj.rolling_ball.vel.y = ((*b)->obj.rolling_ball.vel.y) + (v_rel_n * n.y);

    // Compute the speed of a and b as the lengths of their velocities
    double speedA = phylib_length((*a)->obj.rolling_ball.vel);
    double speedB = phylib_length((*b)->obj.rolling_ball.vel);

    // if the speed is greater
    // than PHYLIB_VEL_EPSILON then set the acceleration of the ball to the negative
    // velocity divided by the speed multiplied by PHYLIB_DRAG
    if (speedA > PHYLIB_VEL_EPSILON){
        (*a)->obj.rolling_ball.acc.x = (-1) * (*a)->obj.rolling_ball.vel.x / speedA * PHYLIB_DRAG;
        (*a)->obj.rolling_ball.acc.y = (-1) * (*a)->obj.rolling_ball.vel.y / speedA * PHYLIB_DRAG;
    }
    if (speedB > PHYLIB_VEL_EPSILON){
        (*b)->obj.rolling_ball.acc.x = (-1) * (*b)->obj.rolling_ball.vel.x / speedB * PHYLIB_DRAG;
        (*b)->obj.rolling_ball.acc.y = (-1) * (*b)->obj.rolling_ball.vel.y / speedB * PHYLIB_DRAG;
    }
}

unsigned char phylib_rolling( phylib_table *t ){

    unsigned char count = 0;

    for (int f = 0; f < PHYLIB_MAX_OBJECTS; f++){
        if ((*t).object[f] != NULL){
            if ((*t).object[f]->type == PHYLIB_ROLLING_BALL){
                count++;
            }
        }
    }
    return count;
}

phylib_table *phylib_segment( phylib_table *table ){

    if (phylib_rolling(table) == 0){ // Return NULL if there are no rollingBalls
        return NULL;
    }
    else{
        phylib_table *segmentedTable = phylib_copy_table(table);
        double g = 0;
        
        for (g = PHYLIB_SIM_RATE; g < PHYLIB_MAX_TIME; g+= PHYLIB_SIM_RATE){
            for (int h = 0; h < PHYLIB_MAX_OBJECTS; h++){
                if ((*segmentedTable).object[h] != NULL && (*segmentedTable).object[h]->type == 1){
                    phylib_roll((*segmentedTable).object[h], (*table).object[h], g);
                }
            }
            (*segmentedTable).time = (*table).time + g;
            // Loop should end if:
            // The phylib_distance between the ball and another phylib_object is less than 0.0.
            // If this happens, apply the phylib_bounce function to the ball and the object
            if (checkBounce(segmentedTable) == 1){
                return segmentedTable;
            }

            // A ROLLING_BALL has stopped
            if (checkStop(segmentedTable) == 1){
                return segmentedTable;
            }
        }
        return segmentedTable;
    }
}

unsigned char checkBounce(phylib_table *table){

    double distance = 0.0;
    int check = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if ((*table).object[i] != NULL && (*table).object[i]->type == 1){
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                if ((*table).object[j] != NULL && i != j){
                    distance =  phylib_distance((*table).object[i], (*table).object[j]);

                    if (distance < 0.0){
                        phylib_bounce(&table->object[i], &table->object[j]);
                        return 1;
                    }
                }
            }
        }
    }
    return check;
}

unsigned char checkStop(phylib_table *table){

    int check = 0;

    for (int l = 0; l < PHYLIB_MAX_OBJECTS; l++){
        if ((*table).object[l] != NULL && (*table).object[l]->type == 1){
            check = phylib_stopped((*table).object[l]);
            if (check == 1){
                return check;
            }
        }
    }
    return check;
}

char *phylib_object_string( phylib_object *object ){
static char string[80];
if (object==NULL)
{
sprintf( string, "NULL;" );
return string;
}
switch (object->type)
{
case PHYLIB_STILL_BALL:
sprintf( string,
"STILL_BALL (%d,%6.1lf,%6.1lf)",
object->obj.still_ball.number,
object->obj.still_ball.pos.x,
object->obj.still_ball.pos.y );
break;
case PHYLIB_ROLLING_BALL:
sprintf( string,
"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
object->obj.rolling_ball.number,
object->obj.rolling_ball.pos.x,
object->obj.rolling_ball.pos.y,
object->obj.rolling_ball.vel.x,
object->obj.rolling_ball.vel.y,
object->obj.rolling_ball.acc.x,
object->obj.rolling_ball.acc.y );
break;
case PHYLIB_HOLE:
sprintf( string,
"HOLE (%6.1lf,%6.1lf)",
object->obj.hole.pos.x,
object->obj.hole.pos.y );
break;
case PHYLIB_HCUSHION:
sprintf( string,
"HCUSHION (%6.1lf)",
object->obj.hcushion.y );
break;
case PHYLIB_VCUSHION:
sprintf( string,
"VCUSHION (%6.1lf)",
object->obj.vcushion.x );
break;
}
return string;
}
