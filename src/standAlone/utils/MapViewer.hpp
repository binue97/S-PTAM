/**
 * Authors: Binue
 */

#pragma once

#include <opencv2/core.hpp>

#include "../../sptam/Map.hpp"


class MapViewer
{
  public:
    MapViewer(int32_t mapWidth, int32_t mapHeight);
    ~MapViewer() = default;

    void setMap(sptam::Map& map);

    void drawMap();

    double scale_ = 8.0;
    cv::Point2i offset_;

  private:
    void clear();

    void drawTrajectory();

    void drawLandmarks();

    static void mouseCallback(int32_t event, int32_t x, int32_t y, int32_t flags, void* data);

    cv::Point2i world_to_image(const Eigen::Vector3d& point_world) const;

    cv::Size mapSize_;
    cv::Mat canvas_;
    sptam::Map* mapPtr_;
};
